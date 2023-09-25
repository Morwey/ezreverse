import numpy as np
# import cv2 
from skimage import color, util, io, exposure
# import colorsys
from PIL import Image, ImageOps
from shiny import App, render, ui, reactive
from shiny.types import FileInfo, ImgData, SilentException
from ttohsl import *
from color_change import adjust_colors
import os
from convolve import apply_kernel

def ensure_non_negative(image):
    return exposure.rescale_intensity(image, out_range=(0, 1))

app_ui = ui.page_fluid(
    ui.h2("Playing with invert"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_radio_buttons('demos', 'Examples',
                    choices = {"demo1": "Example1", "demo2": "Example2", "upload": "Upload image"}),
            ui.panel_conditional("input.demos === 'upload'", 
                    ui.input_file("file", "Choose a file to upload:", multiple=True),
            ),
            ui.input_radio_buttons('func', 'Functions',
                    choices = {"invert": "Invert", "bc": "Bacground color change"}),
            ui.panel_conditional("input.func === 'bc'", 
                ui.input_radio_buttons("bcspace", "Color space",choices=
                                   {'rgb':'RGB'})),
            ui.panel_conditional("input.func === 'invert'", 
                ui.input_radio_buttons("cspace", "Color space",choices=
                                   {'hls':'HLS',
                                    'yiq':'YIQ', 
                                    'lab':'CIElab'})),
            ui.input_radio_buttons('kernel', 'Convolve Kernel',
                    choices={'none':'None', 'blur':'Blur', 'edge':'Edge detection', 'sharpen':'Sharpen'}),
            ui.input_slider('gamma',"Gamma correctness",value=1, min=0, max=5,step=0.1),
            ui.input_action_button("reset", "Reset"),
            ui.panel_conditional("input.func === 'bc'", 
                    ui.input_selectize("bcolor", "Background color", 
                                       ['white', 'black', 'grey']), #'transparent'
                    ui.input_slider("threshold", "Threshold", value=10, min=0, max=20,step=0.5)
            ),
        ),
        ui.panel_main(
            ui.output_text("instruction"),
            ui.output_plot("image")
        )
    )
)

def server(input, output, session):

    @reactive.Effect
    @reactive.event(input.reset)
    def _():
        print('reset')
        ui.update_slider(
            "gamma",
            # label=f"Gamma correctness. Current value: {1}",
            value=1,
        )

    @reactive.Effect
    def _():
        ui.update_slider(
            "gamma",
            label=f"Gamma correctness. Current value: {input.gamma()}",
        )

    @output
    @render.text
    def instruction():
        if(input.demos() == 'upload'):
            return "Please upload image"
        else:
            pass


    @output
    @render.image
    async def image() -> ImgData:
        file_infos: list[FileInfo] = input.file()
        if input.demos() == 'demo1' or input.demos() == 'demo2':
            path = f'demo_input/{input.demos()}.png'
            image_data = io.imread(path)
            image_data = np.array(image_data)
            # raise SilentException()
        else:
            if not file_infos:
                return 
            file_info = file_infos[0]
            img = Image.open(file_info["datapath"])
            # Convert to numpy array for skimage processing
            image_data = np.array(img)

        image_data = image_data[:, :, :3]

        if input.kernel() != 'none':
            image_data_kernel = apply_kernel(image_data, input.kernel())
        else:
            image_data_kernel = image_data.copy()
            
        if input.func() == 'invert':
            if input.cspace() == "rgb":
                negative_image = util.invert(image_data_kernel)
            elif input.cspace() == "hls": 
                hls_image = rgb_to_hls(image_data_kernel)
                negative_image = hls_image.copy()
                negative_image[:, :, 1] = 1 - negative_image[:, :, 1]
                #print(np.max(negative_image),np.min(negative_image))
                negative_image = hls_to_rgb(negative_image)
                print(np.max(negative_image),np.min(negative_image))
            elif input.cspace() == "hsv":
                hsv_image = rgb_to_hsv(image_data_kernel)
                negative_image = hsv_image.copy()
                negative_image[:, :, 0] = 1 - negative_image[:, :, 0]
                negative_image = hsv_to_rgb(negative_image)
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
            negative_image = adjust_colors(img_array=image_data_kernel, 
                                           color=input.bcolor(),space='rgb',
                                           threshold = input.threshold())

        negative_image = exposure.adjust_gamma(ensure_non_negative(negative_image), gamma=input.gamma())                   
        
        # Save for render.image
        
        if not os.path.exists("test_results"):
            os.makedirs("test_results")
        io.imsave("test_results/inverted.png", util.img_as_ubyte(negative_image))
        print('run once')
        negative_image = io.imread('test_results/inverted.png')
        # concatenated_image = cv2.hconcat([image_data,negative_image]) 
        height1, width1 = image_data.shape[:2]
        height2, width2 = negative_image.shape[:2]
        new_image_np = np.zeros((max(height1, height2), width1 + width2, 3), dtype=np.uint8)
        new_image_np[:height1, :width1] = image_data[:,:,:3]
        new_image_np[:height2, width1:] = negative_image
        io.imsave("test_results/combin-inverted.png", util.img_as_ubyte(new_image_np))
        return {"src": "test_results/combin-inverted.png", "width": "100%"}


app = App(app_ui, server)
