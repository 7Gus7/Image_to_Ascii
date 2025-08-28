#!/usr/bin/env python3

import sys
import os
from PIL import Image

# 95 characters (watch out for escape characters!)
# Generated order via order_chars.py
ascii_brightness = " `.-':,_\"^~;><!=*\\/+r?cL|)(vT7iJzsl}{xt[Y]Fnu1IfC3jo25eakSyVhPEwZK4XU69pbqdmAHRG#OD%8WNB$M0gQ&@"


def scale(pixels):
    # Ask to scale
    scale = input("\nWould you like to scale the image? [y/n]: ")
    while scale == '' or scale[0].lower() not in "yn":
        scale = input("\nINVALID INPUT.\nWould you like to scale the image? [y/n]: ")

    if scale[0].lower() == "y":
        # Which way would they like to scale by?
        print(f"Currently, the image dimensions are {len(pixels[0])} wide by {len(pixels)} tall ({((len(pixels[0])**2) + (len(pixels)**2))**2} diagonally)")
        scale = input("\nScale the image vertically, horizontally, or diagonally? [v/h/d]: ")
        while scale == '' or scale[0].lower() not in "vhd":
            scale = input("\nINVALID INPUT.\nScale the image vertically, horizontally, or diagonally? [v/h/d]: ")

        # Scale in 1 of the 3 ways!
        if scale[0].lower() == "v":
            scale = input(f"\nEnter a new character height for the image (currently {len(pixels)}): ")
            while not scale.isdigit() or 0 > int(scale):
                scale = input(f"\nINVALID INPUT.\nEnter a new character height for the image (currently {len(pixels)}): ")
        
        elif scale[0].lower() == "h":
            scale = input(f"\nEnter a new character width for the image (currently {len(pixels[0])}): ")
            while not scale.isdigit() or 0 > int(scale):
                scale = input(f"\nINVALID INPUT.\nEnter a new character width for the image (currently {len(pixels[0])}): ")
        
        
            scale = int(scale)
            if (scale[0].lower() == "v" and scale < len(pixels)) or (scale[0].lower() == "h" and scale < len(pixels[0])):
                scale_down(pixels, scale, "v") # TODO
            elif scale > len(pixels):
                scale_up(pixels, scale, "v") # TODO, if we scale_up after a scale_down, should we return the image to its original state first to raise quality?

    return pixels



def manipulate_pixels(img):

    # Ask to invert brightness
    invert_brightness(pixels)

    # Ask for minimum brightness value
    threshold_val = get_threshold()
    if threshold_val:
        pixels = [p if p >= threshold_val else 0 for p in pixels]

    # Bound values into the range of ascii characters we have available
    pixels = [p * (len(ascii_brightness) -1) // 255 for p in pixels] # p/255 = x/ascii rank => x = p * ascii rank/255

    # Ask to crop image and scale
    pixels = [pixels[i * width:(i+1) * width] for i in range(height)] # Get list of rows of pixel values for output
    pixels = crop(pixels) # Geeky ahh list comprehensions won't let me modify the list in the crop function
    #pixels = scale(pixels) #TODO

    return pixels



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
        input_img = input("\nPlease enter the filename of your image: ") # TODO Add an option to cancel and go back
    
    while os.path.isfile(input_img) == False or input_img[-4:] != ".png": # TODO Might be able to change this to any image file...
        input_img = input("\nFILE NOT FOUND!\nPlease enter the filename of your image: ")

    # Get image into something managable
    image_file = Image.open(input_img)
    image_file = image_file.convert('L') # Convert image to grayscale
    # image_file.save('result.png')

    return image_file



def write_img(ascii_art_img, edits, print_output=True):
    # Apply edits first
    working_copy = [row[:] for row in ascii_art_img]
    if edits["minimum_thres"] != 0 or edits["maximum_thres"] != 255: # Brightness thresholds
            working_copy = [[p if edits["minimum_thres"] <= p and p <= edits["maximum_thres"] else edits["fill_thres"] for p in row] for row in ascii_art_img]


    # Output row-by-row
    # Requires that ascii list is formatted like [[row][row][row]]
    if print_output:
        print()
    else:
        output = open("output.txt", "w") # TODO ask user for output file name
        
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
            edits["fill_thres"], edits["minimum_thres"] = 0
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
                print("Pro tip: A value of 0 won't change anything.")
            else: # Likewise
                input_option = f"\nInput a maximum brightness value between {edits["minimum_thres"]} to 255: "
                boundaries = [edits["minimum_thres"], 255]
                print("Pro tip: A value of 255 won't change anything.")
            
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
        print("6 - Reset croppings")
        print("7 - Go back")
        print(f"\nCURRENT crops: {edits["crop_l"]} (left), {edits["crop_r"]} (right), {edits["crop_t"]} (top), {edits["crop_b"]} (bottom).")

        user_choice = input("\nPlease select a number: ")
        while not user_choice.isdigit() or not (1 <= int(user_choice) and int(user_choice) <= 7):
            user_choice = input("\nINVALID INPUT.\nPlease select a number: ")

        # Now with user input, we can run their choice
        if int(user_choice) == 7:
            if [edits["crop_l"], edits["crop_r"], edits["crop_t"], edits["crop_b"]] != beginning_thresholds:
                print("\nCROPPING SAVED!")
                return True
            return False
        
        elif int(user_choice) == 6:
            edits["crop_l"], edits["crop_r"], edits["crop_t"], edits["crop_b"] = 0
            print("\nRESET THRESHOLDS!") # Reset

        elif int(user_choice) == 5:
            write_img(pixels, edits) # Display ascii art
        
        else: # Adjust croppings
            if int(user_choice) == 1: # Left, make sure to not exceed past the current right crop
                input_option = f"\nHow many characters would you like to crop off the left? Enter a value between 0 and {len(pixels[0]) - edits["crop_r"]}: " #LEFT OFF HERE
                boundaries = [0, edits["maximum_thres"]]
                print("Pro tip: A value of 0 won't change anything.")
            elif int(user_choice) == 2: # Likewise for right
                input_option = f"\nInput a maximum brightness value between {edits["minimum_thres"]} to 255: "
                boundaries = [edits["minimum_thres"], 255]
                print("Pro tip: A value of 255 won't change anything.")
            
            # Ask for pixel value
            brightness_threshold = input(input_option)
            while not brightness_threshold.isdigit() or not (boundaries[0] <= int(brightness_threshold) and int(brightness_threshold) <= boundaries[1]):
                brightness_threshold = input(f"\nINVALID INPUT.{input_option}")
                
            if int(user_choice) == 1:
                edits["minimum_thres"] = int(brightness_threshold)
            else:
                edits["maximum_thres"] = int(brightness_threshold)



    # Ask to crop
    crop = input("\nWould you like to crop the image? [y/n]: ")
    while crop == '' or crop[0].lower() not in "yn":
        crop = input("\nINVALID INPUT.\nWould you like to crop the image? [y/n]: ")

    if crop[0].lower() == "y":
        # Crop each side
        directions = ["left", "right", "top", "bottom"]
        for direction in directions:
            if direction == "left" or direction == "right":
                far_bound = len(pixels[0])
            else:
                far_bound = len(pixels)
            
            crop = input(f"\nHow many characters would you like to crop off the {direction}? Enter a value between 0 to {far_bound}: ")
            while not crop.isdigit() or not (0 <= int(crop) and int(crop) <= far_bound):
                crop = input(f"\nINVALID INPUT.\nHow many characters would you like to crop off the {direction}? Enter a value between 0 to {far_bound}: ")

            crop = int(crop)
            if crop == 0:
                continue # No need to crop 0 pixels
            
            # Remove pixels from respective side
            if direction == "left":
                pixels = [row[crop:] for row in pixels if row]
            elif direction == "right":
                pixels = [row[:-crop] for row in pixels if row]
            elif direction == "top":
                pixels = pixels[crop:]
            else:            # bottom
                pixels = pixels[:-crop]

    return pixels



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
    edits = {"minimum_thres": 0, "maximum_thres": 255, "fill_thres": 0, "crop_l": 0, "crop_r": 0, "crop_t": 0, "crop_b": 0, "scale_x": None, "scale_y": None}

    # Infinite loop until user is finished making the ascii art
    while True:
        option = show_menu(img)

        if option == 1:
            # TODO Check if we are overwriting a save by accident
            # if saved == False and img == None:...

            saved = False
            img = get_img(img==None)

            # Get list of rows formatted like [[row][row][row]] of pixel values for output
            pixels = list(img.getdata())
            edits["scale_x"], edits["scale_y"] = img.size
            pixels = [pixels[i * edits["scale_x"]:(i+1) * edits["scale_x"]] for i in range(edits["scale_y"])]
            

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
            pass
            # saved = not crop(pixels, edits) and saved

        elif option == 7:
            saved = False

        elif option == 8:
            if exit_program(saved):
                break
                
        

        
        # TODO
        # add image scaling
        # add undo option
        # add help menu
        # Allow user to change order of Ascii character brightnesses (for other fonts)
        # Instead of linear [y/n] questioning, make it terminal prompt like, probably using regex
        # ascii_art_img = manipulate_pixels(img)

    print("\nEXITING PROGRAM... Goodbye!")



if __name__ == "__main__":
    main()
