import numpy as np

color_space = {'hsl':{'channel':1,'limit':1},
               'lab':{'channel':0,'limit':'100'}}

def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip('#')
    return list(int(hex_value[i:i+2], 16) for i in (0, 2, 4))


def adjust_colors(img_array, color='white', space='rgb',custom='#ffffff',threshold = 30, reverse = False):

    color_map = {'white': [255, 255, 255], 'black': [0, 0, 0], 'grey': [123, 123, 123]}
    if space == 'rgb':
        # Find pixels where the difference between max and min channel value is <= 20
        # mask = np.abs(np.max(img_array, axis=-1) - np.min(img_array, axis=-1)) <= 50
        mask = np.std(img_array, axis=-1) <= threshold

    # Set those pixels to the desired color
    new_img_array = img_array.copy()
    if color == 'Hexadecimal RGB':
        new_img_array[mask] = hex_to_rgb(custom)
    elif reverse:
        new_img_array[mask] = 255 - new_img_array[mask]
    else:
        new_img_array[mask] = color_map[color]

    return new_img_array
