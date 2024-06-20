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
from modules.spin import rotate_rgb
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
    ui.head_content(ui.include_js("custom.js")),
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
    ui.page_navbar(
        shinyswatch.theme.journal(),
        ui.nav('App',
            ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_radio_buttons('demos', 'Data',
                            choices = {"demo1": "Example: Cells",
                                        "demo2": "Example: Graph", 
                                        "demo3": "Example: Synthetic data", 
                                        "upload": "Upload image"}),
                    ui.panel_conditional("input.demos === 'upload'", 
                            ui.input_file("file", "Choose a file to upload:", multiple=True),
                    ),
                    ui.input_radio_buttons('func', 'Action',
                            choices = {"invert": "Invert background", "bc": "Replace background color"}),
                    ui.panel_conditional("input.func === 'invert'", 
                        ui.input_radio_buttons("cspace", "Color space",choices=
                                        {'hls':'HSL',
                                            'yiq':'YIQ', 
                                            'lab':'CIElab',
                                            'rgb':'RGB'})),
                    # ui.input_slider('gamma',"Gamma", value=1, min=0, max=10,step=0.1),
                    ui.input_numeric('gamma',"Gamma", value=1, min=0, max=10,step=0.1),
                    ui.input_slider('spin',"Color rotation",value=0, min=-180, max=180,step=1),
                    ui.panel_conditional("input.func === 'bc'", 
                            ui.input_selectize("bcolor", "Background color", 
                                            ['Reverse','white', 'black', 'grey','custom']), #'transparent'
                            ui.input_slider("threshold", "Threshold", value=10, min=0, max=20,step=0.5)
                    ),
                    ui.panel_conditional("input.bcolor === 'custom'", 
                                        ui.input_text('custom_bc','Custom Background Color',placeholder="Hexadecimal RGB Color, e.g., #11FF33")),
                    ui.input_radio_buttons(
                            "kernel",
                            "Filter",
                            {'none':'None', 'blur':'Blur', 'edge':'Edge detection', 'sharpen':'Sharpen'},
                        ),
                    ui.input_action_button("resetcolor", "Reset"),
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
            ui.nav("About",ui.img(src="logo_color.png", style="width: 13%;"),
            ui.markdown("""
            ### EZreverse - Efficient and Robust Background Modifier
            An online tool for image background manipulation including inverting the background without changing the original colors, and changing the background color.
                                       
            #### Features
            - **Invert Background**: Without altering the original colors, this function transforms the RGB image into different color spaces including HSL, YIQ, LAB, and inverts their corresponding lightness channels to invert the background, and transfrom back to RGB image.
            - **Change Background Color**: By calculating the standard deviation of RGB values of each pixel in an image and using a specific threshold, this function filters out images with gray backgrounds and reverse/change it.
            - EZreverse provides multiple **kernels**, including blur, edge detection, and sharpening, as well as the option to customize the **gamma** value to fine-tune saturation. 
            
            #### Contact                        
            EZreverse is created and maintained by Joachim Goedhart and Xinwei Song
            Bug reports and feature requests can be communicated in several ways:
            Github: [EZreverse/issues](https://github.com/Morwey/ezreverse/issues)
                                       
            #### Source
            The source code can be obtained [here](https://github.com/Morwey/ezreverse).                       
            """
            )), #,title='EZreverse'
            )
    )


def server(input, output, session):

    @reactive.Effect
    @reactive.event(input.reset)
    def _():
        ui.update_slider(
            "gamma",
            value=1,
        )

    @reactive.Effect
    @reactive.event(input.resetcolor)
    def _():
        ui.update_slider( 
            "spin",
            value=0,
        )
        ui.update_numeric( #_slider( 
            "gamma",
            value=1,
        )
        ui.update_radio_buttons(
            "kernel",
            selected='none'
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
        return path
    
    @reactive.Calc
    def read():
        if input.demos() != 'upload':
            path = f'demo_input/{input.demos()}.png'
        elif input.file():
            path = up()
        return path
    
    @reactive.Calc
    def invert():
        p.set(1, message="Reading iamge")
        try:
            image_data = np.array(io.imread(read()))
            image_data = image_data[:, :, :3]
            
            if len(image_data.shape) != 3 or image_data.shape[2] != 3 or image_data.size == 0:
                raise ValueError("Only three-channel images (e.g., PNG, JPEG) are supported.")
        except Exception as e:
            raise ValueError("Only three-channel images (e.g., PNG, JPEG) are supported.") from e

        if input.kernel() != 'none':
            p.set(2, message="Applying kernel")
            image_data_kernel = apply_kernel(image_data, input.kernel())
        else:
            p.set(2, message="Reversing")
            image_data_kernel = image_data.copy()

        image_data_kernel = util.img_as_ubyte(np.clip(image_data_kernel, 0, 255)/255)

        p.set(3, message="Reversing")

        if input.func() == 'invert':
            conversion_func = conversion_funcs.get(input.cspace(), None)
            negative_image = conversion_func(image_data_kernel)
        elif input.func() == 'bc':
            reverse = True if input.bcolor() == 'Reverse' else None
            color_value = 'Hexadecimal RGB' if input.bcolor() == 'custom' else input.bcolor()
            custom_value = input.custom_bc() if input.bcolor() == 'custom' else None

            negative_image = adjust_colors(
                img_array=image_data_kernel,
                color=color_value,
                space='rgb',
                threshold=input.threshold(),
                custom=custom_value,
                reverse = reverse)
        
        print('run one time')
        return negative_image
    
    @output
    @render.plot
    def image() -> ImgData:
        global p, colortune, file_path
        with ui.Progress(min=1, max=6) as p:
            if input.bcolor() == 'custom' and not input.custom_bc():
                return
            if input.file() or input.demos() != 'upload':
                p.set(message="Reverse in progress", detail="This may take a while...")
                negative_image = invert()
            else:
                return
            
            if input.gamma() != 1:
                p.set(4, message="Gamma correcting")
                negative_image = exposure.adjust_gamma(ensure_non_negative(negative_image), gamma=input.gamma())
            else:
                p.set(4, message="Almost done")

            negative_image = util.img_as_ubyte(np.clip(negative_image, 0, 255))

            if input.spin() != 0:
                p.set(5, message="Rotating color")
                colortune = negative_image.copy()
                negative_image = rotate_rgb(colortune, input.spin())

            fig, ax = plt.subplots()
            ax.imshow(negative_image)
            ax.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove any padding
            fig.patch.set_visible(False)

            p.set(5, message="Almost done")
        return fig

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
    @render.plot
    def ori():
        file: list[FileInfo] | None = input.file()
        if input.bcolor() == 'custom' and not input.custom_bc():
            return
        if input.demos() != 'upload' or input.file():
            path = read()
        else:
            return
        with reactive.isolate():
            try:
                image_data = np.array(io.imread(path))
                fig, ax = plt.subplots()
                ax.imshow(image_data)
                ax.axis('off')
                plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove any padding
                fig.patch.set_visible(False)
                return fig
            except Exception as e:
                raise ValueError("Only three-channel images (e.g., PNG, JPEG) are supported.") from e

    @session.download(
        filename=f"InvertImage.png"
    )
    async def download():
        await asyncio.sleep(0.25)
        # file_path = "test_results/inverted.png"
        img = io.imread(file_path)
        pil_img = Image.fromarray(img.astype(np.uint8))
    
        img_byte_array = BytesIO()
        pil_img.save(img_byte_array, format='PNG')
        
        # Return byte stream
        yield img_byte_array.getvalue()
        
    
www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)


