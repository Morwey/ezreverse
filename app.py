import numpy as np
import asyncio
# import cv2 
from skimage import color, util, io, exposure
# import colorsys
from PIL import Image, ImageOps
from shiny import App, render, ui, reactive
from shiny.types import FileInfo, ImgData, SilentException
from ttohsl import *
from color_change import adjust_colors
import os
from io import BytesIO
from convolve import apply_kernel
import matplotlib.pyplot as plt

def invert_hls(image_data):
    hls_image = rgb_to_hls(image_data)
    inverted_image = hls_image.copy()
    inverted_image[:, :, 1] = 1 - inverted_image[:, :, 1]
    return hls_to_rgb(inverted_image)

def invert_yiq(image_data):
    yiq_image = rgb_to_yiq(image_data)
    negative_image = yiq_image.copy()
    negative_image[:, :, 0] = 1 - negative_image[:, :, 0]
    return yiq_to_rgb(negative_image)

conversion_funcs = {
    'rgb': util.invert,
    'hls': invert_hls,
    'yiq': invert_yiq,
}

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
                                       ['white', 'black', 'grey','custom']), #'transparent'
                    ui.input_slider("threshold", "Threshold", value=10, min=0, max=20,step=0.5)
            ),
            ui.panel_conditional("input.bcolor === 'custom'", 
                                 ui.input_text('custom_bc','Custom Backgound Color')),
            ui.download_button('download', 'Export Image')
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
        # print('reset')
        ui.update_slider(
            "gamma",
            # label=f"Gamma correctness. Current value: {1}",
            value=1,
        )

    @reactive.Effect
    def _():
        if input.cspace() == 'lab':
            ui.update_radio_buttons("kernel",choices = {'none':'None'})
        elif input.bcspace() == 'rgb' and input.func() == 'bc' or input.cspace() == 'hls':
            ui.update_radio_buttons("kernel",choices = {'none':'None','blur':'Blur'})
        else:
            ui.update_radio_buttons("kernel",
                    choices = {'none':'None','blur':'Blur', 'edge':'Edge detection', 'sharpen':'Sharpen'})

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
        elif input.bcolor() == 'custom' and input.custom_bc() == '':
            return 'Please enter color'
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
            conversion_func = conversion_funcs.get(input.cspace(), None)
            negative_image = conversion_func(image_data_kernel)
        elif input.func() == 'bc':
            if input.bcolor() == 'custom' and not input.custom_bc():
                return

            # Set the color based on whether it's custom or not
            color_value = 'Hexadecimal RGB' if input.bcolor() == 'custom' else input.bcolor()
            custom_value = input.custom_bc() if input.bcolor() == 'custom' else None

            negative_image = adjust_colors(
                img_array=input.threshold(),
                color=color_value,
                space='rgb',
                threshold=input.threshold(),
                custom=custom_value)

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

    @session.download(
        filename=f"InvertImage.png"
    )
    async def download():
        await asyncio.sleep(0.25)
        file_path = "test_results/inverted.png"
        img = io.imread(file_path)
        pil_img = Image.fromarray(img.astype(np.uint8))
    
        img_byte_array = BytesIO()
        pil_img.save(img_byte_array, format='PNG')
        
        # Return byte stream
        yield img_byte_array.getvalue()
        
    

app = App(app_ui, server)


