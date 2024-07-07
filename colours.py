from enum import Enum
from math import sqrt


# given a BGR pixel from opencv, compare it to known colours and get the one it matches
class Colour(Enum):
    # rough BGR values, they seemingly change based on where on the screen they are
    NONE = None
    RED = [5, 5, 180]
    BLUE = [150, 95, 15]
    YELLOW = [10, 175, 185]
    BLACK = [10, 10, 10]
    MENU_CORNER_TRIM = [245, 130, 35]
    MP_GREEN = [10, 250, 15]
    MP_RED = [5, 5, 190]
    TEXTBOX_BG = [210, 225, 230]
    NAME_BOX_BG = [100, 100, 100]


def get_colour_fuzzy(pixels):
    """
    Get the first recognized colour from a list of colours.
    Expected to represent a 3x3, where index 4 is the primary pixel.

    :param pixels: array of BGR values
    :return: first recognized colour in the list, or NONE if not found
    """
    c = get_colour(pixels[4])
    if c != Colour.NONE:
        return c
    for pixel in pixels:
        c = get_colour(pixel)
        if c != Colour.NONE:
            return c
    return Colour.NONE


def get_colour(pixel):
    move_colour = get_move_colour(pixel)
    # return a colour if the pixel is very close in BGR value
    if move_colour != Colour.NONE:
        return move_colour
    elif colour_dist(pixel, Colour.MENU_CORNER_TRIM.value) < 20:
        return Colour.MENU_CORNER_TRIM
    elif colour_dist(pixel, Colour.TEXTBOX_BG.value) < 20:
        return Colour.TEXTBOX_BG
    else:
        return get_mp_colour(pixel)


def get_mp_colour_fuzzy(pixels):
    """
    Get the first recognized MP colour from a list of colours.
    Expected to represent a 3x3, where index 4 is the primary pixel.

    :param pixels: array of BGR values
    :return: first recognized MP colour in the list, or NONE if not found
    """
    c = get_mp_colour(pixels[4])
    if c != Colour.NONE:
        return c
    for pixel in pixels:
        c = get_mp_colour(pixel)
        if c != Colour.NONE:
            return c
    return Colour.NONE


def get_mp_colour(pixel):
    if pixel[1] > 200 and pixel[0] < 50 and pixel[2] < 50:
        return Colour.MP_GREEN
    elif pixel[2] > 100 and pixel[0] < 50 and pixel[1] < 50:
        return Colour.MP_RED
    else:
        return Colour.NONE


def get_move_colour_fuzzy(pixels):
    """
    Get the first recognized move colour from a list of colours.
    Expected to represent a 3x3, where index 4 is the primary pixel.

    :param pixels: array of BGR values
    :return: first recognized move colour in the list, or NONE if not found
    """
    c = get_move_colour(pixels[4])
    if c != Colour.NONE:
        return c
    for pixel in pixels:
        c = get_move_colour(pixel)
        if c != Colour.NONE:
            return c
    return Colour.NONE


def get_move_colour(pixel):
    if colour_dist(pixel, Colour.RED.value) < 20:
        return Colour.RED
    elif colour_dist(pixel, Colour.BLUE.value) < 20:
        return Colour.BLUE
    elif colour_dist(pixel, Colour.YELLOW.value) < 20:
        return Colour.YELLOW
    else:
        return Colour.NONE


def colour_dist(c1, c2):
    # Euclidean distance of vector in R3
    return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)
