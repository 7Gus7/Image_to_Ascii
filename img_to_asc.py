#!/usr/bin/env python3

import sys
import os
from PIL import Image, UnidentifiedImageError

# 95 characters (watch out for escape characters!)
# Generated order via order_chars.py
ascii_brightness = " `.-':,_\"^~;><!=*\\/+r?cL|)(vT7iJzsl}{xt[Y]Fnu1IfC3jo25eakSyVhPEwZK4XU69pbqdmAHRG#OD%8WNB$M0gQ&@"


def show_menu(img):
    if img == None:
        # The program doesn't have an image to work with yet
        print("Welcome to the Image to Ascii Converter!")

        if len(sys.argv) == 2:
            print(f"Image file provided in command line: {sys.argv[1]}")
        else:
            print("First things first, let's select an image to convert...")
        
        return 1

    # Program has a picture to work with now
    print("\nMAIN MENU OPTIONS:")
    print("1 - Change photo")
    print("2 - Display ascii art")
    print("3 - Save ascii art to file")
    print("4 - Invert brightness")
    print("5 - Adjust brightness threshold")
    print("6 - Crop")
    print("7 - Scale")
    print("8 - Exit program")

    user_choice = input("\nPlease select a number: ")
    while not user_choice.isdigit() or not (1 <= int(user_choice) and int(user_choice) <= 8):
        user_choice = input("\nINVALID INPUT.\nPlease select a number: ")

    return int(user_choice)



def get_img(new_image=True):
    # Get name of file
    if len(sys.argv) == 2 and new_image:
        input_img = sys.argv[1]
    else:
        input_img = input("\nPlease enter the name of your image file: ")
    
    while True:
        while not os.path.isfile(input_img):
            input_img = input("\nFILE NOT FOUND!\nPlease enter the name of your image file: ")

        # Get image into something managable
        try:
            image_file = Image.open(input_img)
            image_file = image_file.convert('L') # Convert image to grayscale
            break
        except UnidentifiedImageError:
            print("\nNOT A VALID IMAGE FILE!", end="")
            input_img = ""
    
    # image_file.save('result.png')
    return image_file



def scale_matrix(matrix, new_width, new_height):
    # Helper function for scaling, called from write_img
    result = []
    for y in range(new_height): # Iterating through each (now scaled) height level
        # We are going to find a source pixel (x, y) to map into our new scaled image
        src_y = int(y * len(matrix) / new_height) # y/new_height = src_y/original height => src_y = y * original height/new_height
        row = []
        for x in range(new_width): # Iterating through each (now scaled) row position
            src_x = int(x * len(matrix[0]) / new_width) # x/new_width = src_x/original width => src_x = x * original width/new_width
            row.append(matrix[src_y][src_x])
        result.append(row)
    return result



def write_img(ascii_art_img, edits, print_output=True):
    # APPLY EDITS FIRST
    working_copy = [row[:] for row in ascii_art_img]
    if edits["minimum_thres"] != 0 or edits["maximum_thres"] != 255: # Brightness thresholds
        working_copy = [[p if edits["minimum_thres"] <= p and p <= edits["maximum_thres"] else edits["fill_thres"] for p in row] for row in ascii_art_img]
    
    # Crop edits, remove pixels from respective sides
    if edits["crop_l"]: working_copy = [row[edits["crop_l"]:] for row in working_copy if row]
    if edits["crop_r"]: working_copy = [row[:-edits["crop_r"]] for row in working_copy if row]
    if edits["crop_t"]: working_copy = working_copy[edits["crop_t"]:]
    if edits["crop_b"]: working_copy = working_copy[:-edits["crop_b"]]

    # Scale to new size
    new_width = int(len(working_copy[0]) * float(edits["scale_x"]/100))
    new_height = int(len(working_copy) * float(edits["scale_y"]/100))
    if new_width != len(working_copy[0]) or new_height != len(working_copy):
        working_copy = scale_matrix(working_copy, new_width, new_height)  # Helper function because I went down a rabbit hole


    # Output row-by-row
    # Requires that ascii list is formatted like [[row][row][row]]
    if print_output:
        print()
    else:
        output = open("output.txt", "w")
        
    # Iterate through rows of pixels
    for row in working_copy:
        for pixel in row:
            # Bound values into the range of ascii characters we have available
            pixel = pixel * (len(ascii_brightness) -1) // 255 # p/255 = x/ascii rank => x = p * ascii rank/255

            if print_output:
                print(ascii_brightness[pixel], end="")
            else:
                output.write(ascii_brightness[pixel])

        # Next row
        if print_output:
            print()
        else:
            output.write("\n")
    
    if print_output:
        input("\nPRESS ENTER TO CONTINUE...")
    else:
        output.close()
        print("\nIMAGE SAVED!")



def invert_brightness(pixels):
    # Ask to invert brightness
    invert = input("\nWould you like to invert the image brightness? [y/n]: ")
    while invert == '' or invert[0].lower() not in "yn":
        invert = input("\nINVALID INPUT.\nWould you like to invert the image brightness? [y/n]: ")

    # Flip the numbers around if yes
    # Probably should do this in the application phase in write_img... meh whatever
    if invert[0].lower() == "y":
        for row in range(len(pixels)):
            for pixel in range(len(pixels[0])):
                pixels[row][pixel] = 255 - pixels[row][pixel] # Pixel values are from 0-255
    


def adjust_brightness_threshold(pixels, edits):
    beginning_thresholds = [edits["minimum_thres"], edits["maximum_thres"], edits["fill_thres"]]
    
    # Sub menu for min and max brightness thresholds
    while True:
        print("\nBRIGHTNESS THRESHOLD OPTIONS:")
        print("1 - Adjust minimum brightness")
        print("2 - Adjust maximum brightness")
        print("3 - Change fill brightness")
        print("4 - Display ascii art")
        print("5 - Reset ascii art brightness")
        print("6 - Go back")
        print(f"\nCURRENT BRIGHTNESS THRESHOLDS: {edits["minimum_thres"]} (minimum), {edits["maximum_thres"]} (maximum).")

        user_choice = input("\nPlease select a number: ")
        while not user_choice.isdigit() or not (1 <= int(user_choice) and int(user_choice) <= 6):
            user_choice = input("\nINVALID INPUT.\nPlease select a number: ")

        # Now with user input, we can run their choice
        if int(user_choice) == 6:
            if [edits["minimum_thres"], edits["maximum_thres"], edits["fill_thres"]] != beginning_thresholds:
                print("\nBRIGHTNESS THRESHOLD SETTINGS SAVED!")
                return True
            return False
        
        elif int(user_choice) == 5:
            edits["fill_thres"] = 0
            edits["minimum_thres"] = 0
            edits["maximum_thres"] = 255
            print("\nRESET THRESHOLDS!") # Reset

        elif int(user_choice) == 4:
            write_img(pixels, edits) # Display ascii art

        elif int(user_choice) == 3:
            # Ask for brightness to fill with
            print("\nWhen characters are cut because they don't meet the threshold requirements, they are replaced with empty space (brightness = 0) by default.")
            fill = input("Enter a brightness between 0 (default) to 255 as filler: ")
            while not fill.isdigit() or not (0 <= int(fill) and int(fill) <= 255):
                if len(fill) == 0:
                    fill = "0"
                else:
                    fill = input(f"\nINVALID INPUT.\nEnter a brightness between 0 (default) to 255 as filler: ")
            edits["fill_thres"] = int(fill)

        else:
            if int(user_choice) == 1: # Adjust min, make sure to not exceed past the current maximum brightness
                input_option = f"\nInput a minimum brightness value between 0 to {edits["maximum_thres"]}: "
                boundaries = [0, edits["maximum_thres"]]
                print("\nPro tip: A value of 0 won't change anything.")
            else: # Likewise
                input_option = f"\nInput a maximum brightness value between {edits["minimum_thres"]} to 255: "
                boundaries = [edits["minimum_thres"], 255]
                print("\nPro tip: A value of 255 won't change anything.")
            
            # Ask for pixel value
            brightness_threshold = input(input_option)
            while not brightness_threshold.isdigit() or not (boundaries[0] <= int(brightness_threshold) and int(brightness_threshold) <= boundaries[1]):
                brightness_threshold = input(f"\nINVALID INPUT.{input_option}")
                
            if int(user_choice) == 1:
                edits["minimum_thres"] = int(brightness_threshold)
            else:
                edits["maximum_thres"] = int(brightness_threshold)



def crop(pixels, edits):
    beginning_thresholds = [edits["crop_l"], edits["crop_r"], edits["crop_t"], edits["crop_b"]]
    
    # Sub menu for cropping
    while True:
        print("\nCROPPING OPTIONS:")
        print("1 - Crop left")
        print("2 - Crop right")
        print("3 - Crop top")
        print("4 - Crop bottom")
        print("5 - Display ascii art")
        print("6 - Reset crop")
        print("7 - Go back")
        print(f"\nCURRENT PIXELS CROPPED: {edits["crop_l"]} (left), {edits["crop_r"]} (right), {edits["crop_t"]} (top), {edits["crop_b"]} (bottom).")

        user_choice = input("\nPlease select a number: ")
        while not user_choice.isdigit() or not (1 <= int(user_choice) and int(user_choice) <= 7):
            user_choice = input("\nINVALID INPUT.\nPlease select a number: ")

        # Now with user input, we can run their choice
        if int(user_choice) == 7:
            if [edits["crop_l"], edits["crop_r"], edits["crop_t"], edits["crop_b"]] != beginning_thresholds:
                print("\nCROP SAVED!")
                return True
            return False
        
        elif int(user_choice) == 6:
            edits["crop_l"] = 0
            edits["crop_r"] = 0
            edits["crop_t"] = 0
            edits["crop_b"] = 0
            print("\nRESET CROPS!") # Reset

        elif int(user_choice) == 5:
            write_img(pixels, edits) # Display ascii art
        
        else: # Adjust crops, do note that cropping gets rendered before scaling, so we are only cropping pixels from the original image
            input_option = "\nHow many pixels from the original image would you like to crop off the "
            if int(user_choice) == 1: # Left, make sure to not exceed past the current right crop
                input_option += "left? "
                boundary = len(pixels[0]) - edits["crop_r"]
            elif int(user_choice) == 2: # Likewise for right
                input_option += "right? "
                boundary = len(pixels[0]) - edits["crop_l"]
            elif int(user_choice) == 3: # Likewise for top
                input_option += "top? "
                boundary = len(pixels) - edits["crop_b"]
            elif int(user_choice) == 4: # Likewise for bottom
                input_option += "bottom? "
                boundary = len(pixels) - edits["crop_t"]
            input_option += f"Enter a value between 0 and {boundary}: "
            
            if boundary == 0:
                print("\nNo more space to crop! Try adjusting the crop on the other side first...") # TODO make messages like these go under the menu when it next reappears
            else: # Ask for crop amount
                print("\nPro tip: A value of 0 won't crop anything.")
                crop = input(input_option)
                while not crop.isdigit() or not (0 <= int(crop) and int(crop) <= boundary):
                    crop = input(f"\nINVALID INPUT.{input_option}")

                if int(user_choice) == 1: # Update left crop
                    edits["crop_l"] = int(crop)
                elif int(user_choice) == 2: # Right crop
                    edits["crop_r"] = int(crop)
                elif int(user_choice) == 3: # Top crop
                    edits["crop_t"] = int(crop)
                elif int(user_choice) == 4: # Bottom crop
                    edits["crop_b"] = int(crop)



def scale(pixels, edits):
    beginning_thresholds = [edits["scale_x"], edits["scale_y"]]
    
    # Sub menu for scaling
    while True:
        print("\nSCALING OPTIONS:")
        print("1 - Scale")
        print("2 - Scale width only")
        print("3 - Scale height only")
        print("4 - Display ascii art")
        print("5 - Reset scale")
        print("6 - Go back")
        print(f"\nCURRENT SCALE: {edits["scale_x"]}% (width), {edits["scale_y"]}% (height)")

        user_choice = input("\nPlease select a number: ")
        while not user_choice.isdigit() or not (1 <= int(user_choice) and int(user_choice) <= 6):
            user_choice = input("\nINVALID INPUT.\nPlease select a number: ")

        # Now with user input, we can run their choice
        if int(user_choice) == 6:
            if [edits["scale_x"], edits["scale_y"]] != beginning_thresholds:
                print("\nSCALING SAVED!")
                return True
            return False
        
        elif int(user_choice) == 5:
            edits["scale_x"] = 100
            edits["scale_y"] = 100
            print("\nRESET SCALE!") # Reset

        elif int(user_choice) == 4:
            write_img(pixels, edits) # Display ascii art
        
        else: # Adjust scale
            print("\nPro tip: A value of 100% is the original size of the image.")
            if int(user_choice) == 1 or int(user_choice) == 2: # Select new width
                scale_width = input(f"\nEnter a percentage for width (currently {edits["scale_x"]}): ")
                while not scale_width.isdigit() or int(scale_width) < 0:
                    scale_width = input(f"\nINVALID INPUT.\nEnter a percentage for width (currently {edits["scale_x"]}): ")
                edits["scale_x"] = int(scale_width)

            if int(user_choice) == 1 or int(user_choice) == 3: # Select new height
                keep_ratio = "n"
                if int(user_choice) == 1: # If doing a diagonal, give the option to keep the aspect ratio
                    keep_ratio = input("\nWould you like to keep the same aspect ratio? [y/n]: ")
                    while keep_ratio == '' or keep_ratio[0].lower() not in "yn":
                        keep_ratio = input("\nINVALID INPUT.\nWould you like to keep the same aspect ratio? [y/n]: ")
                    
                if keep_ratio[0].lower() == "n": # Ask for new height
                    scale_height = input(f"\nEnter a percentage for height (currently {edits["scale_y"]}): ")
                    while not scale_height.isdigit() or int(scale_height) < 0:
                        scale_height = input(f"\nINVALID INPUT.\nEnter a percentage for height (currently {edits["scale_y"]}): ")
                else: # Keep aspect ratio
                    scale_height = scale_width
                edits["scale_y"] = int(scale_height)



def exit_program(saved):
    # Confirm to exit without saving
    if not saved:
        confirm_exit_message = "\nAre you sure you want to exit without saving your current ascii art? [y/n]: "
    else:
        confirm_exit_message = "\nAre you sure you want to exit? [y/n]: "

    exiting = input(confirm_exit_message)
    while exiting == '' or exiting[0].lower() not in "yn":
        exiting = input(f"\nINVALID INPUT.\n{confirm_exit_message}")

    if exiting[0].lower() == "y":
        return 1 # Confirmed exit
    else:
        return 0



def main():
    img = None
    edits = {"minimum_thres": 0, "maximum_thres": 255, "fill_thres": 0, "crop_l": 0, "crop_r": 0, "crop_t": 0, "crop_b": 0, "scale_x": 100, "scale_y": 100}

    # Infinite loop until user is finished making the ascii art
    while True:
        option = show_menu(img)

        if option == 1:
            # Check if we are overwriting a save by accident
            new_image = "y"
            if img != None and saved == False: # Short circuited on the first go-around
                new_image = input("\nAre you sure you want to change the photo before saving your current ascii art? [y/n]: ")
                while new_image == '' or new_image[0].lower() not in "yn":
                    new_image = input("\nINVALID INPUT.\nAre you sure you want to change the photo before saving your current ascii art? [y/n]: ")

            if new_image[0].lower() == "y":
                saved = False
                img = get_img(img==None)

                # Get list of rows formatted like [[row][row][row]] of pixel values for output
                pixels = list(img.getdata())
                width, height = img.size
                pixels = [pixels[i * width:(i+1) * width] for i in range(height)]
            
        elif option == 2:
            write_img(pixels, edits) # Display ascii art

        elif option == 3:
            write_img(pixels, edits, print_output=False) # Save ascii art to file
            saved = True

        elif option == 4:
            invert_brightness(pixels)
            saved = False

        elif option == 5:
            saved = not adjust_brightness_threshold(pixels, edits) and saved
            
        elif option == 6:
            saved = not crop(pixels, edits) and saved

        elif option == 7:
            saved = not scale(pixels, edits) and saved

        elif option == 8:
            if exit_program(saved):
                break

        
        # TODO
        # Next version:
        # Improve the location of menu text (such as warnings, notifications like IMAGE SAVED! and such)
        # ask user for output file name
        # add undo option
        # add help menu
        # Allow user to change order of Ascii character brightnesses (for other fonts)
        # Regex in addition to number select

    print("\nEXITING PROGRAM... Goodbye!")



if __name__ == "__main__":
    main()
