import numpy as np
import asyncio
# import cv2 
from skimage import util, io, exposure
# import colorsys
from PIL import Image, ImageOps
from shiny import App, render, ui, reactive
from shiny.types import FileInfo, ImgData, SilentException
from modules.color_change import adjust_colors
import os
from io import BytesIO
from modules.convolve import apply_kernel
import matplotlib.pyplot as plt
from modules.invert import *
from htmltools import Tag
from pathlib import Path
import shinyswatch

conversion_funcs = {
    'rgb': util.invert,
    'hls': invert_hls,
    'yiq': invert_yiq,
    'lab': invert_lab
}
path_invert = "test_results/inverted.png"
path_ori = "test_results/ori.png"

def ensure_non_negative(image):
    return exposure.rescale_intensity(image, out_range=(0, 1))

app_ui = ui.page_fluid(
    ui.tags.style(
        """
        .app-col {
            border: 1px solid black;
            border-radius: 5px;
            background-color: #EEF0F2; 
            padding: 8px;
            margin-top: 5px;
            margin-bottom: 5px;
        }
        """
    ),
    ui.img(src="logo.png", style="width: 13%;"),
    ui.page_navbar(
        # shinyswatch.theme.journal(),
        ui.nav('App',
            ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_radio_buttons('demos', 'Examples',
                            choices = {"demo1": "Example1", "demo2": "Example2", "upload": "Upload image"}),
                    ui.panel_conditional("input.demos === 'upload'", 
                            ui.input_file("file", "Choose a file to upload:", multiple=True),
                    ),
                    ui.input_radio_buttons('func', 'Functions',
                            choices = {"invert": "Invert", "bc": "Bacground color change"}),
                    ui.panel_conditional("input.func === 'invert'", 
                        ui.input_radio_buttons("cspace", "Color space",choices=
                                        {'hls':'HLS',
                                            'yiq':'YIQ', 
                                            'lab':'CIElab',
                                            'rgb':'RGB'})),
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
                ),
                ui.panel_main(
                    ui.download_button('download', 'Export Image'),
                    ui.row(
                        ui.column(6,ui.div({"class": "app-col"},
                                ui.output_text("instruction"),
                                ui.output_plot("image"))),
                        ui.column(6,ui.div({"class": "app-col"},
                                ui.output_text("instruori"),
                                ui.output_plot('ori')))
                                ))
                )
            ),
            ui.nav("About",ui.markdown("""
            ## Background Modifier

            A simple online tool for image background manipulation including inverting the background without changing the original colors, and changing the background color.

            ### Features

            - **Invert Background**: Without altering the original colors, this function transforms the RGB image into different color spaces like YIQ, HSL, LAB, and inverts their corresponding channels.
            - **Change Background Color**: By calculating the standard deviation of RGB values of each pixel in an image and using a specific threshold, this function filters out images that possibly have black or white backgrounds.

            ### Usage

            Visit [here](https://amsterdamstudygroup.shinyapps.io/invertimage/) to use the tool online.
            """
            ))
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
    '''
    @reactive.Effect
    def _():
        if input.cspace() == 'lab':
            ui.update_radio_buttons("kernel",choices = {'none':'None'})
        elif input.func() == 'bc' or input.cspace() == 'hls':
            ui.update_radio_buttons("kernel",choices = {'none':'None','blur':'Blur'})
        else:
            ui.update_radio_buttons("kernel",
                    choices = {'none':'None','blur':'Blur', 'edge':'Edge detection', 'sharpen':'Sharpen'})
    '''

    @reactive.Effect
    def _():
        ui.update_slider(
            "gamma",
            label=f"Gamma correctness. Current value: {input.gamma()}",
        )

    @output
    @render.text
    def instruction():
        if input.demos() == 'upload' and not input.file():
            return "Please upload image"
        elif input.bcolor() == 'custom' and input.custom_bc() == '':
            return 'Please enter color'
        else:
            return f'Reversed image:'

    @reactive.Calc
    def up():
        global path
        file_infos = input.file()
        path = file_infos[0]["datapath"]
        img = Image.open(path)
        print('upload one time')
        return img
    
    @reactive.Calc
    def read():
        if input.demos() == 'demo1' or input.demos() == 'demo2':
            path = f'demo_input/{input.demos()}.png'
            image_data = np.array(io.imread(path))
        else:
            img = up()
            image_data = np.array(img)

        image_data = image_data[:, :, :3]
        return image_data
    
    @reactive.Calc
    def invert():
        image_data = read()

        if input.kernel() != 'none':
            image_data_kernel = apply_kernel(image_data, input.kernel())
        else:
            image_data_kernel = image_data.copy()

        if input.func() == 'invert':
            conversion_func = conversion_funcs.get(input.cspace(), None)
            negative_image = conversion_func(image_data_kernel)
        elif input.func() == 'bc':
            color_value = 'Hexadecimal RGB' if input.bcolor() == 'custom' else input.bcolor()
            custom_value = input.custom_bc() if input.bcolor() == 'custom' else None

            negative_image = adjust_colors(
                img_array=image_data_kernel,
                color=color_value,
                space='rgb',
                threshold=input.threshold(),
                custom=custom_value)
        
        print('run one time')
        return negative_image

    @output
    @render.image
    def image() -> ImgData:
        if input.bcolor() == 'custom' and not input.custom_bc():
            return
        if input.file() or input.demos() != 'upload':
            negative_image = invert()
        else:
            return

        negative_image = exposure.adjust_gamma(ensure_non_negative(negative_image), gamma=input.gamma())
        
        io.imsave("test_results/inverted.png", util.img_as_ubyte(negative_image))
        negative_image = io.imread(path_invert)
        return {"src": path_invert,"width": "100%"} #"width": "100%"
    
    @output
    @render.text
    def instruori():
        if input.demos() == 'upload' and not input.file():
            return "Please upload image"
        elif input.bcolor() == 'custom' and input.custom_bc() == '':
            return 'Please enter color'
        else:
            return 'Original image:'
        
    @output
    @render.image
    def ori():
        if input.bcolor() == 'custom' and not input.custom_bc():
            return
        if input.file() or input.demos() != 'upload':
            image_data = read()
        else:
            return
        with reactive.isolate():
            io.imsave(path_ori, util.img_as_ubyte(image_data))
        return {"src": path_ori,"width": "100%"} #, "width": "100%"

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
        
    
www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)


