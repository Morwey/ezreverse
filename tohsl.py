import numpy as np
import colorsys
from skimage import io
import matplotlib.pyplot as plt

def rgb_to_hsl(img_rgb):
    img_rgb = img_rgb / 255.0
    img_hsl = np.zeros(img_rgb.shape)
    for i in range(img_rgb.shape[0]):
        for j in range(img_rgb.shape[1]):
            r, g, b = img_rgb[i, j]
            h, l, s = colorsys.rgb_to_hls(r, g, b)
            img_hsl[i, j, 0] = h
            img_hsl[i, j, 1] = s
            img_hsl[i, j, 2] = l
    return img_hsl

def hsl_to_rgb(img_hsl):
    img_rgb = np.zeros_like(img_hsl, dtype=np.uint8)
    
    for i in range(img_hsl.shape[0]):
        for j in range(img_hsl.shape[1]):
            h, s, l = img_hsl[i, j]
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            img_rgb[i, j] = [int(r * 255), int(g * 255), int(b * 255)]
            
    return img_rgb

'''
img_rgb = io.imread('/Users/songxinwei/Desktop/shinyProject/oRGB.png')
img_hsl = rgb_to_hsl(img_rgb)
img_rgb = hsl_to_rgb(img_hsl)

plt.imshow(img_rgb)
plt.show()
'''
