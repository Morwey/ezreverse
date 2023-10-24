import numpy as np
from scipy.signal import convolve2d
from PIL import Image
from skimage import io

def apply_kernel_to_channel(channel, kernel):
    return convolve2d(channel, kernel, mode='same', boundary='wrap')

def convolve_rgb(image, kernel):
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    r_conv = apply_kernel_to_channel(r, kernel)
    g_conv = apply_kernel_to_channel(g, kernel)
    b_conv = apply_kernel_to_channel(b, kernel)
    return np.stack([r_conv, g_conv, b_conv], axis=-1)

def apply_kernel(image, operation):
    kernels = {
        "blur": np.array([[1, 2, 1],
                          [2, 4, 2],
                          [1, 2, 1]]) / 16,
        
        "edge_x": np.array([[-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1]]),
        
        "edge_y": np.array([[-1, -2, -1],
                            [0, 0, 0],
                            [1, 2, 1]]),
        
        "sharpen": np.array([[0, -1,0], [-1, 5, -1], [0, -1, 0]])
    }

    if operation == "edge":
        edges_x = convolve_rgb(image, kernels["edge_x"])
        edges_y = convolve_rgb(image, kernels["edge_y"])
        return np.sqrt(edges_x**2 + edges_y**2)
    else:
        kernel = kernels.get(operation, None)
        return convolve_rgb(image, kernel)
