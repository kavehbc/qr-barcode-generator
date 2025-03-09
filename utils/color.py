def hex_to_rgba(hex_color, alpha):
    # output would be similar to (0, 0, 0, 255)
    hex_color = hex_color.lstrip("#")
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    lst_rgb = list(rgb)
    lst_rgb.append(alpha)
    rgba = tuple(lst_rgb)
    return rgba


def make_transparent(img, opaque_pixel, transparent_pixel):
    # invert colors and set alpha color
    img_data = img.getdata()
    new_pixels = []
    for item in img_data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:  # if white pixel
            new_pixels.append(transparent_pixel)
        else:
            new_pixels.append(opaque_pixel)
    img.putdata(new_pixels)
    return img

def make_image(img, fill_color, back_color):
    # invert colors and set alpha color
    img_data = img.getdata()
    new_pixels = []
    for item in img_data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:  # if white pixel
            new_pixels.append(back_color)
        else:
            new_pixels.append(fill_color)
    img.putdata(new_pixels)
    return img
