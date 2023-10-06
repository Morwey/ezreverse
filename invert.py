from ttohsl import *
from skimage import color

def invert_hls(image_data):
    hls_image = rgb_to_hls(image_data)
    inverted_image = hls_image.copy()
    inverted_image[:, :, 1] = 1 - inverted_image[:, :, 1]
    return hls_to_rgb(inverted_image)

def invert_yiq(image_data):
    yiq_image = rgb_to_yiq(image_data)
    negative_image = yiq_image.copy()
    negative_image[:, :, 0] = 1 - negative_image[:, :, 0]
    return yiq_to_rgb(negative_image)

def invert_lab(image_data):
    lab_image = color.rgb2lab(image_data)
    negative_lab_image = lab_image.copy()
    negative_lab_image[:, :, 0] = 100 - negative_lab_image[:, :, 0] 
    # negative_image = (negative_lab_image * 255).astype(np.uint8)
    return color.lab2rgb(negative_lab_image)