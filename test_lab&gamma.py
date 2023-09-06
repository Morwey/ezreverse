import numpy as np
import cv2
from skimage import color, util, io, exposure

def cv2_invert(iamge_path = 'demo_input/oRGB.png'):
    rgb_image = cv2.imread('demo_input/oRGB.png')
    lab_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2Lab)
    '''
    print(f' max{np.max(lab_image[:, :, 0])}, min{np.min(lab_image[:, :, 0])}')
    print(f' max{np.max(lab_image[:, :, 1])}, min{np.min(lab_image[:, :, 1])}')
    print(f' max{np.max(lab_image[:, :, 2])}, min{np.min(lab_image[:, :, 2])}')
    '''
    lab_image[:, :, 0] = 255 - lab_image[:, :, 0] # range
    rgb_image = cv2.cvtColor(lab_image, cv2.COLOR_Lab2RGB)

    '''
    print(f' max{np.max(rgb_image[:, :, 0])}, min{np.min(rgb_image[:, :, 0])}')
    print(f' max{np.max(rgb_image[:, :, 1])}, min{np.min(rgb_image[:, :, 1])}')
    print(f' max{np.max(rgb_image[:, :, 2])}, min{np.min(rgb_image[:, :, 2])}')
    '''

    # lab_image = exposure.adjust_gamma(lab_image, gamma=1)
    cv2.imwrite('test_results/cv2invert_test_image.jpg', rgb_image)

def sk_invert(iamge_path = 'demo_input/oRGB.png'):

    rgb_image = io.imread('demo_input/oRGB.png')
    lab_image = color.rgb2lab(rgb_image)

    lab_image[:, :, 0] = 100 - lab_image[:, :, 0] # range
    rgb_image = color.lab2rgb(lab_image)

    rgb_image = exposure.adjust_gamma(rgb_image, gamma=1)

    io.imsave("test_results/skinvert_test_image.png", util.img_as_ubyte(rgb_image))

cv2_invert()
sk_invert()

