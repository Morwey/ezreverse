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

'''
            
        if input.func() == 'invert':
            if input.cspace() == "rgb":
                negative_image = util.invert(image_data_kernel)
            elif input.cspace() == "hls": 
                hls_image = rgb_to_hls(image_data_kernel)
                negative_image = hls_image.copy()
                negative_image[:, :, 1] = 1 - negative_image[:, :, 1]
                #print(np.max(negative_image),np.min(negative_image))
                negative_image = hls_to_rgb(negative_image)
            elif input.cspace() == "yiq":
                yiq_image = rgb_to_yiq(image_data_kernel)
                negative_image = yiq_image.copy()
                negative_image[:, :, 0] = 1 - negative_image[:, :, 0]
                negative_image = yiq_to_rgb(negative_image)
            elif input.cspace() == "lab":
                lab_image = color.rgb2lab(image_data_kernel)
                negative_lab_image = lab_image.copy()
                negative_lab_image[:, :, 0] = 100 - negative_lab_image[:, :, 0] 
                # negative_image = (negative_lab_image * 255).astype(np.uint8)
                negative_image = color.lab2rgb(negative_lab_image)
        elif input.func() == 'bc':
            if input.bcolor() == 'custom':
                # print(f'bs is {input.custom_bc()}')
                if input.custom_bc() == '':
                    return
                else:
                    negative_image = adjust_colors(img_array=image_data_kernel, 
                                           color='Hexadecimal RGB',space='rgb',
                                           threshold = input.threshold(),
                                           custom = input.custom_bc())
            else:
                negative_image = adjust_colors(img_array=image_data_kernel, 
                                           color=input.bcolor(),space='rgb',
                                           threshold = input.threshold())

            elif input.cspace() == "hsv":
                hsv_image = rgb_to_hsv(image_data_kernel)
                negative_image = hsv_image.copy()
                negative_image[:, :, 0] = 1 - negative_image[:, :, 0]
                negative_image = hsv_to_rgb(negative_image)
                
                
'''
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