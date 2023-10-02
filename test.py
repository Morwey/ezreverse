from PIL import Image
from skimage import color, util, io, exposure
from tohsl import *

image = io.imread('/Users/songxinwei/Desktop/shiny/demo_input/demo2.png')

image = image[:, :, :3]

hsl_image = rgb_to_hls(image)
negative_image = hsl_image.copy()
# negative_image[:, :, 1] = 1 - negative_image[:, :, 1]
# print(negative_image)
negative_image = hls_to_rgb(negative_image)

print(negative_image)
'''
background = Image.new('RGB', image.size, (255, 255, 255))

merged_image = Image.alpha_composite(background, image.convert('RGBA'))

merged_image.save('Users/songxinwei/Desktop/shiny/demo_input/demo2_test.png.jpg', 'JPEG')
'''