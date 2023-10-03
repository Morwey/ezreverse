import numpy as np
import colorsys

def custom_rgb_to_hls(r, g, b):
    sumc = r + g + b
    if np.abs(sumc - 2) < 0.05:
        return 0, 0.5, 0  
    elif np.abs(sumc) < 0.05:
        return 0, 0, 0
    else:
        return colorsys.rgb_to_hls(r, g, b)

# Using Numpy's built-in functionality for broadcasting
def rgb_to_hls(rgb_image):
    rgb_image = rgb_image.astype(float) / 255.0
    hls_image = np.apply_along_axis(lambda x: custom_rgb_to_hls(*x), -1, rgb_image)
    return hls_image

def hls_to_rgb(hls_image):
    rgb_converter = np.vectorize(colorsys.hls_to_rgb)
    r, g, b = rgb_converter(hls_image[..., 0], hls_image[..., 1], hls_image[..., 2])
    return np.stack([r, g, b], axis=-1) * 255

def rgb_to_colorspace(rgb_image, conversion_func):
    rgb_image = rgb_image.astype(float) / 255.0
    converted_image = np.vectorize(conversion_func)(rgb_image[..., 0], rgb_image[..., 1], rgb_image[..., 2])
    return np.stack(converted_image, axis=-1)

def colorspace_to_rgb(color_image, conversion_func):
    rgb_converter = np.vectorize(conversion_func)
    r, g, b = rgb_converter(color_image[..., 0], color_image[..., 1], color_image[..., 2])
    return np.stack([r, g, b], axis=-1) * 255

def rgb_to_hsv(rgb_image):
    return rgb_to_colorspace(rgb_image, colorsys.rgb_to_hsv)

def hsv_to_rgb(hsv_image):
    return colorspace_to_rgb(hsv_image, colorsys.hsv_to_rgb)

def rgb_to_yiq(rgb_image):
    return rgb_to_colorspace(rgb_image, colorsys.rgb_to_yiq)

def yiq_to_rgb(yiq_image):
    return colorspace_to_rgb(yiq_image, colorsys.yiq_to_rgb)

'''
def custom_rgb_to_hls(r, g, b):
    sumc = r + g + b
    if np.abs(sumc - 2) < 0.05:
        return 0, 0.5, 0  
    elif np.abs(sumc) < 0.05:
        return 0, 0, 0
    else:
        return colorsys.rgb_to_hls(r, g, b)

# Using Numpy's built-in functionality for broadcasting
def rgb_to_hls(rgb_image):
    rgb_image = rgb_image.astype(float) / 255.0
    hls_image = np.apply_along_axis(lambda x: custom_rgb_to_hls(*x), -1, rgb_image)
    return hls_image

def hls_to_rgb(hls_image):
    rgb_converter = np.vectorize(colorsys.hls_to_rgb)
    r, g, b = rgb_converter(hls_image[..., 0], hls_image[..., 1], hls_image[..., 2])
    return np.stack([r, g, b], axis=-1) * 255

def rgb_to_colorspace(rgb_image, conversion_func):
    rgb_image = rgb_image.astype(float) / 255.0
    converted_image = np.vectorize(conversion_func)(rgb_image[..., 0], rgb_image[..., 1], rgb_image[..., 2])
    return np.stack(converted_image, axis=-1)

def colorspace_to_rgb(color_image, conversion_func):
    rgb_converter = np.vectorize(conversion_func)
    r, g, b = rgb_converter(color_image[..., 0], color_image[..., 1], color_image[..., 2])
    return np.stack([r, g, b], axis=-1) * 255

def rgb_to_hsv(rgb_image):
    return rgb_to_colorspace(rgb_image, colorsys.rgb_to_hsv)

def hsv_to_rgb(hsv_image):
    return colorspace_to_rgb(hsv_image, colorsys.hsv_to_rgb)

def rgb_to_yiq(rgb_image):
    return rgb_to_colorspace(rgb_image, colorsys.rgb_to_yiq)

def yiq_to_rgb(yiq_image):
    return colorspace_to_rgb(yiq_image, colorsys.yiq_to_rgb)
'''