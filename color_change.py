import numpy as np
from skimage import io

"""
Adjust pixels in an RGB image where the maximum difference between R, G, and B values is <= 5.

Args:
- img_array (np.array): A 3D numpy array representing an RGB image.

Returns:
- np.array: The adjusted image array.
"""

# need improve faster
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