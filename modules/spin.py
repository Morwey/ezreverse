from PIL import Image
import numpy as np
import math

def rotate_rgb(img_data, angle):
    """
    Rotate the RGB color space of the image.

    :param image_path: Path to the image file.
    :param angle: Rotation angle in degrees.
    :return: Rotated Image object.
    """
    angle_rad = math.radians(angle)

    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    rotation_matrix = np.array([
        [cos_a + (1.0 - cos_a) / 3.0, 1.0 / 3.0 * (1.0 - cos_a) - math.sqrt(1.0 / 3.0) * sin_a, 1.0 / 3.0 * (1.0 - cos_a) + math.sqrt(1.0 / 3.0) * sin_a],
        [1.0 / 3.0 * (1.0 - cos_a) + math.sqrt(1.0 / 3.0) * sin_a, cos_a + 1.0 / 3.0 * (1.0 - cos_a), 1.0 / 3.0 * (1.0 - cos_a) - math.sqrt(1.0 / 3.0) * sin_a],
        [1.0 / 3.0 * (1.0 - cos_a) - math.sqrt(1.0 / 3.0) * sin_a, 1.0 / 3.0 * (1.0 - cos_a) + math.sqrt(1.0 / 3.0) * sin_a, cos_a + 1.0 / 3.0 * (1.0 - cos_a)]
    ])

    # Apply the rotation matrix to each pixel
    rotated_img_data = np.dot(img_data.reshape((-1, 3)), rotation_matrix).reshape(img_data.shape)

    # Ensure the values are still within [0, 255]
    rotated_img_data = np.clip(rotated_img_data, 0, 255).astype(np.uint8)

    # Create a new Image object with the rotated data
    rotated_img = Image.fromarray(rotated_img_data)

    return rotated_img
