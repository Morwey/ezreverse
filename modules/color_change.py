import numpy as np

color_space = {'hsl':{'channel':1,'limit':1},
               'lab':{'channel':0,'limit':'100'}}

def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip('#')
    return list(int(hex_value[i:i+2], 16) for i in (0, 2, 4))

# Vectorized! much more faster

def adjust_colors(img_array, color='white', space='rgb',custom='#ffffff',threshold = 30):

    color_map = {'white': [255, 255, 255], 'black': [0, 0, 0], 'grey': [123, 123, 123]}
    if space == 'rgb':
        # Find pixels where the difference between max and min channel value is <= 20
        # mask = np.abs(np.max(img_array, axis=-1) - np.min(img_array, axis=-1)) <= 50
        mask = np.std(img_array, axis=-1) <= threshold

    '''
    elif space == 'hsl':
        # mask = ((img_array[..., 0] < 10) & (img_array[..., 2] < 10)) #| (img_array[..., 1] < 0.1) | (img_array[..., 1] > 0.9)
        # mask = (img_array[..., 2] < 0) | (img_array[..., 2] > 255) | ((img_array[..., 0] < 100)&(img_array[..., 1] <100))
        mask = (img_array[..., 1] < 4) | (img_array[..., 1] > 253)
        # print(np.max(img_array[..., 0]), np.min(img_array[..., 0])) all are 0,255
    elif space == 'lab':
        # mask = (img_array[..., 1] < 8) & (img_array[..., 2] < 8)
        # subset = img_array[..., 1:3]; mask = np.std(subset, axis=-1) <= 1
        mask = np.abs(img_array[..., 1] - img_array[..., 2]) <= threshold'''

    # Set those pixels to the desired color
    new_img_array = img_array.copy()
    if color == 'Hexadecimal RGB':
        new_img_array[mask] = hex_to_rgb(custom)
    else:
        new_img_array[mask] = color_map[color]

    return new_img_array



'''
def adjust_colors(img_array, color = 'white'):

    color_map = {'white':[255,255,255], 'black':[0,0,0], 'grey':[123,123,123]}

    # Loop through the first and second dimensions of the image array
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            pixel = img_array[i, j]
            if np.max(pixel) - np.min(pixel) <= 20:
                img_array[i, j] = color_map[color]
                
    return img_array
'''


'''
# Test the function
img = io.imread('oRGB.png')
print(img[1,1,:])

adjusted_img = adjust_colors(img,"white")
print(adjusted_img[1,1,:])
'''

''' probabaly faster method
def adjust_colors(img_array, color = 'white'):

    color_map = {'white':[255,255,255], 'black':[0,0,0], 'grey':[123,123,123]}

    # Create a mask where the maximum difference between R, G, and B values of a pixel is <= 5
    print(np.abs(img_array - np.roll(img_array, shift=-1, axis=-1)) <= 5)
    mask = np.abs(img_array - np.roll(img_array, shift=-1, axis=-1)) <= 5
    mask_combined = np.all(mask, axis=-1)
    
    # Apply the mask and set the matched pixels to white
    img_array[mask_combined] = [255,255,255]
    
    return img_array
'''