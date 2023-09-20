import numpy as np
import colorsys

def rgb_to_hsl(rgb_image):
    rgb_image = rgb_image.astype(float) / 255.0
    hsl_image = np.vectorize(colorsys.rgb_to_hls)(rgb_image[..., 0], rgb_image[..., 1], rgb_image[..., 2])
    hsl_image = np.stack(hsl_image, axis=-1)
    return hsl_image

def hsl_to_rgb(hsl_image):
    rgb_converter = np.vectorize(colorsys.hls_to_rgb)
    r, g, b = rgb_converter(hsl_image[..., 0], hsl_image[..., 1], hsl_image[..., 2])
    rgb_image = np.stack([r, g, b], axis=-1)

    return (rgb_image * 255).astype(np.uint8) 

def rgb_to_hsv(rgb_image):
    rgb_image = rgb_image.astype(float) / 255.0
    hsv_image = np.vectorize(colorsys.rgb_to_hsv)(rgb_image[..., 0], rgb_image[..., 1], rgb_image[..., 2])
    hsv_image = np.stack(hsv_image, axis=-1)
    return hsv_image

def hsv_to_rgb(hsv_image):
    rgb_converter = np.vectorize(colorsys.hsv_to_rgb)
    r, g, b = rgb_converter(hsv_image[..., 0], hsv_image[..., 1], hsv_image[..., 2])
    rgb_image = np.stack([r, g, b], axis=-1)

    return (rgb_image * 255).astype(np.uint8) 

'''
def rgb_to_yiq(rgb_image):
    rgb_image = rgb_image.astype(float) / 255.0
    yiq_image = np.vectorize(colorsys.rgb_to_yiq)(rgb_image[..., 0], rgb_image[..., 1], rgb_image[..., 2])
    yiq_image = np.stack(rgb_image, axis=-1)
    return yiq_image

def yiq_to_rgb(yiq_image):
    rgb_converter = np.vectorize(colorsys.yiq_to_rgb)
    r, g, b = rgb_converter(yiq_image[..., 0], yiq_image[..., 1], yiq_image[..., 2])
    rgb_image = np.stack([r, g, b], axis=-1)

    return (rgb_image * 255).astype(np.uint8) 
'''

def rgb_to_yiq(rgb_image):
    rgb_image = rgb_image.astype(float) / 255.0
    yiq_converter = np.vectorize(colorsys.rgb_to_yiq)
    y, i, q = yiq_converter(rgb_image[..., 0], rgb_image[..., 1], rgb_image[..., 2])
    yiq_image = np.stack([y, i, q], axis=-1)
    return yiq_image

def yiq_to_rgb(yiq_image):
    rgb_converter = np.vectorize(colorsys.yiq_to_rgb)
    r, g, b = rgb_converter(yiq_image[..., 0], yiq_image[..., 1], yiq_image[..., 2])
    rgb_image = np.stack([r, g, b], axis=-1)

    return (rgb_image * 255).astype(np.uint8)
