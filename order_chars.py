#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont


def render_char_density(ch, font_path="C:/Windows/Fonts/consola.ttf", size=64, show=False):
    # Make grayscale image of character
    img = Image.new("L", (int(size*1.5), int(size*1.5)), color=255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size)

    # Get bounding box of character
    bbox = draw.textbbox((0, 0), ch, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Draw centered
    draw.text(((size - w) // 2, ((size - h) + (size // 4)) // 2), ch, fill=0, font=font)

    # Get pixel counts
    pixels = list(img.getdata())
    black = sum(p for p in pixels)

    print(black, ch)
    if show:
        img.show(title=f"Character: {ch}")
    
    return black


def main():
    img_chars = " `.-':,_\"^~;><!=*\\/+r?cL|)(vT7iJzsl}{xt[Y]Fnu1IfC3jo25eakSyVhPEwZK4XU69pbqdmAHRG#OD%8WNB$M0gQ&@"

    densities = [(ch, render_char_density(ch, "C:/Windows/Fonts/consola.ttf")) for ch in img_chars]

    # Sort lightest to darkest
    sorted_chars = sorted(densities, key=lambda x: x[1], reverse=True)

    print("Characters sorted from lightest to darkest:")
    print("".join(ch for ch, _ in sorted_chars))


if __name__ == "__main__":
    main()
