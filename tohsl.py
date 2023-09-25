import numpy as np
import colorsys

def custom_rgb_to_hls(r, g, b):
    sumc = r + g + b
    if sumc < 2.05 and sumc > 1.95:
        return 0, 0.5, 0  
    elif sumc < 0.05 and sumc > -0.05:
        return 0, 0, 0
    else:
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return h, l, s

def rgb_to_hls(rgb_image):
    rgb_image = rgb_image.astype(float) / 255.0
    hls_image = np.vectorize(custom_rgb_to_hls)(rgb_image[..., 0], rgb_image[..., 1], rgb_image[..., 2])
    hls_image = np.stack(hls_image, axis=-1)
    return hls_image

def hls_to_rgb(hls_image):
    print(np.max(hls_image),np.min(hls_image))
    print(hls_image[300:500,300,:])
    rgb_converter = np.vectorize(colorsys.hls_to_rgb)
    r, g, b = rgb_converter(hls_image[..., 0], hls_image[..., 1], hls_image[..., 2])
    rgb_image = np.stack([r, g, b], axis=-1)
    print(np.max(rgb_image),np.min(rgb_image))

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
