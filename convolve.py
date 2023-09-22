import numpy as np
from scipy.signal import convolve2d
from PIL import Image
import matplotlib.pyplot as plt
from skimage import io

def apply_kernel_to_channel(channel, kernel):
    return convolve2d(channel, kernel, mode='same', boundary='wrap')

def convolve_rgb(image, kernel):
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    r_conv = apply_kernel_to_channel(r, kernel)
    g_conv = apply_kernel_to_channel(g, kernel)
    b_conv = apply_kernel_to_channel(b, kernel)
    return np.stack([r_conv, g_conv, b_conv], axis=-1)

def blur_image(image):
    kernel = np.array([[1, 2, 1],
                       [2, 4, 2],
                       [1, 2, 1]]) / 4500
    return convolve_rgb(image, kernel)

def edge_detection(image):
    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]]) / 300

    kernel_y = np.array([[-1, -2, -1],
                         [0, 0, 0],
                         [1, 2, 1]]) / 300

    edges_x = convolve_rgb(image, kernel_x)
    edges_y = convolve_rgb(image, kernel_y)

    return np.sqrt(edges_x**2 + edges_y**2)

def sharpen_image(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return convolve_rgb(image, kernel)

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
        
        "sharpen": np.array([[0, -1, 0],
                             [-1, 5, -1],
                             [0, -1, 0]])
    }

    if operation == "edge":
        edges_x = convolve_rgb(image, kernels["edge_x"])
        edges_y = convolve_rgb(image, kernels["edge_y"])
        return np.sqrt(edges_x**2 + edges_y**2)
    else:
        kernel = kernels.get(operation, None)
        return convolve_rgb(image, kernel)

'''
image = io.imread('demo_input/demo1.png')
image = np.array(image)
print(image.shape)

blurred_image = apply_kernel(image, 'blur')
edge_detected_image = apply_kernel(image, 'edge')
sharpened_image = apply_kernel(image, 'sharpen')

plt.figure(figsize=(12, 12))

plt.subplot(2, 2, 1)
plt.imshow(image, cmap='gray')
plt.title("Original Image")

plt.subplot(2, 2, 2)
plt.imshow(blurred_image, cmap='gray')
plt.title("Blurred Image")

plt.subplot(2, 2, 3)
plt.imshow(edge_detected_image, cmap='gray')
plt.title("Edge Detected Image")

plt.subplot(2, 2, 4)
plt.imshow(sharpened_image, cmap='gray')
plt.title("Sharpened Image")

plt.tight_layout()
plt.show()
'''