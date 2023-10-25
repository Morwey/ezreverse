import numpy as np
import colorsys

def cs_rgb_to_hls(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    sumc = (maxc+minc)
    rangec = (maxc-minc)
    l = sumc/2.0
    if minc == maxc:
        return 0.0, l, 0.0
    if abs(2.0 - sumc) < 1e-10:  # checking if the value is almost zero
        s = 0.0
    elif l <= 0.5:
        s = rangec / sumc
    else:
        s = rangec / (2.0 - sumc)  # Not always 2.0-sumc: gh-106498.
    rc = (maxc-r) / rangec
    gc = (maxc-g) / rangec
    bc = (maxc-b) / rangec
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, l, s

def rgb_to_hls(rgb_image):
    rgb_image = rgb_image.astype(float) / 255.0
    hls_image = np.vectorize(cs_rgb_to_hls)(rgb_image[..., 0], rgb_image[..., 1], rgb_image[..., 2])
    hls_image = np.stack(hls_image, axis=-1)
    return hls_image

def hls_to_rgb(hls_image):
    rgb_converter = np.vectorize(colorsys.hls_to_rgb)
    r, g, b = rgb_converter(hls_image[..., 0], hls_image[..., 1], hls_image[..., 2])
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
