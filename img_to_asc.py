#!/usr/bin/env python3

import sys
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def open_img():
    if len(sys.argv) != 2:
        input_img = input("Please enter a the filename of your image: ")
    else:
        input_img = sys.argv[1]

    while True:
        try:
            img = mpimg.imread(input_img)
            break
        except:
            input_img = input("Invalid image filename! Please try again: ")

    print(type(img))
    print(img.shape) # Row, Column, Channels (RGB)
    return img




def main():
    img = open_img()

    plt.imshow(img)
    plt.show()



if __name__ == "__main__":
    main()
