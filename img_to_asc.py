#!/usr/bin/env python3

import sys
import os
from PIL import Image

# 95 characters (Watch backslashes here!)
ascii_brightness = (" .`:,;'_^\"><\\/-!~=)(|j?}{][ti+*lv1yrfcJ732uICzwosneaqpgTYVOLxkmhdb54%G9608ZUSA&$PFDQXKRNEH#WBM@")

def get_img():
    # Get name of file
    if len(sys.argv) == 2:
        input_img = sys.argv[1]
    else:
        input_img = input("Please enter the filename of your image: \n")
        while os.path.isfile(input_img) == False or input_img[-4:] != ".png":
            input_img = input("File not found!\nPlease enter the filename of your image: \n")

    # Get image into something managable
    image_file = Image.open(input_img)
    image_file = image_file.convert('L') # Convert image to grayscale
    # image_file.save('result.png')

    return image_file



def invert_grayscale(pixels):
    # Ask to invert grayscale
    invert = input("Would you like to invert the image grayscale? [y/n]: ")
    while invert == '' or invert[0].lower() not in "yn":
        invert = input("Invalid input.\nWould you like to invert the image grayscale? [y/n]: ")

    # Flip the numbers around if yes
    if invert[0].lower() == "y":
        for i in range(len(pixels)):
            pixels[i] = 255 - pixels[i]
    


def get_threshold():
    # Get a value 0-255 that'll be used to blank pixels below that value
    brightness_threshold = input("Would you like to have a minimum brightness threshold? [y/n]: ")
    while brightness_threshold == '' or brightness_threshold[0].lower() not in "yn":

        # Or just accept a number right away
        if brightness_threshold.isdigit() and 0 <= int(brightness_threshold) and int(brightness_threshold) <= 255:
            return int(brightness_threshold)

        brightness_threshold = input("Invalid input.\nWould you like to have a minimum brightness threshold? [y/n]: ")

    # No threshold is the same as threshold = 0
    if brightness_threshold[0].lower() == "n":
        return 0
    

    # Ask for pixel value now
    brightness_threshold = input("Input a brightness value between 0 to 255: ")
    while not brightness_threshold.isdigit() or 0 > int(brightness_threshold) or int(brightness_threshold) > 255:
        brightness_threshold = input("Invalid input.\nInput a brightness value between 0 to 255: ")

    return int(brightness_threshold)



def crop(pixels):
    # Ask to crop
    crop = input("Would you like to crop the image? [y/n]: ")
    while crop == '' or crop[0].lower() not in "yn":
        crop = input("Invalid input.\nWould you like to crop the image? [y/n]: ")

    if crop[0].lower() == "y":
        # Crop each side
        directions = ["left", "right", "top", "bottom"]
        for direction in directions:
            if direction == "left" or direction == "right":
                far_bound = len(pixels[0])
            else:
                far_bound = len(pixels)
            
            crop = input(f"How many characters would you like to crop off the {direction}? Enter a value between 0 to {far_bound}: ")
            while not crop.isdigit() or 0 > int(crop) or int(crop) > far_bound:
                crop = input(f"Invalid input.\nHow many characters would you like to crop off the {direction}? Enter a value between 0 to {far_bound}: ")

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



def manipulate_pixels(img):
    # Get list of image pixels
    pixels = list(img.getdata())
    width, height = img.size

    # Ask to invert grayscale
    invert_grayscale(pixels)

    # Ask for minimum brightness value
    threshold_val = get_threshold()
    if threshold_val:
        pixels = [p if p >= threshold_val else 0 for p in pixels]

    # Bound values into the range of ascii characters we have available
    pixels = [p * (len(ascii_brightness) -1) // 255 for p in pixels] # p/255 = x/ascii rank => x = p * ascii rank/255

    # Ask to crop image
    pixels = [pixels[i * width:(i+1) * width] for i in range(height)] # Get list of rows of pixel values for output
    pixels = crop(pixels) # Geeky ahh list comprehensions won't let me modify the list in the crop function

    return pixels



def write_img(ascii_art_img, print_output=False):
    # Print row-by-row
    with open("output.txt", "w") as output:
        for row in ascii_art_img:
            for pixel in row:
                output.write(ascii_brightness[pixel])
                if print_output: print(ascii_brightness[pixel], end="")
            output.write("\n")
            if print_output: print()



def main():
    img = get_img()

    # TODO
    # add image scaling
    # Instead of linear [y/n] questioning, make it terminal prompt like, probably using regex
    # Also show the result between invert/threshold/scale/crop edits
    ascii_art_img = manipulate_pixels(img)

    write_img(ascii_art_img)



if __name__ == "__main__":
    main()
