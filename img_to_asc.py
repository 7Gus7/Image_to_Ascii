#!/usr/bin/env python3

import sys
import os
from PIL import Image

# 97 characters
ascii_brightness = ("@MBW#HENRKXQDFP$&ASUZ8069G%45bdhmkxLOVYTgpqaensowzCIu237Jcfry1vl*+it[]{}?j|()=~!-/\\<>\"^_';,:`. ")

def convert_img():
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
    image_file.save('result.png')

    pixels = list(image_file.getdata())
    pixels = [-(-p * (len(ascii_brightness)-1) // 255) for p in pixels]
    width, height = image_file.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)] # Get list of rows of pixel values
    
    print(len(ascii_brightness))
    # print(max(pixels))

    with open("output.txt", "w") as output:
        for row in pixels:
            for pixel in row:
                output.write(ascii_brightness[pixel])
                print(ascii_brightness[pixel], end="")
            output.write("\n")
            print()




def main():
    img = convert_img()



if __name__ == "__main__":
    main()
