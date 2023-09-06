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