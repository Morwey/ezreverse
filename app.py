import numpy as np
# import cv2 
from skimage import color, util, io, exposure
# import colorsys
from PIL import Image, ImageOps
from shiny import App, render, ui, reactive
from shiny.types import FileInfo, ImgData, SilentException
from tohsl import rgb_to_hsl, hsl_to_rgb
from color_change import adjust_colors
import os

app_ui = ui.page_fluid(
    ui.h2("Playing with invert"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_file("file", "Choose a file to upload:", multiple=True),
            ui.input_radio_buttons('demos', 'Examples',
                    choices = {"demo1": "Example1", "demo2": "Example2"}),
            ui.input_radio_buttons('func', 'Functions',
                    choices = {"invert": "Invert", "bc": "Background color change"}),
            ui.input_radio_buttons("cspace", "Color space",['hsl','lab','rgb']),
            ui.input_slider('gamma',"Gamma correctness",value=1, min=0, max=2,step=0.1),
            ui.input_action_button("reset", "Reset"),
            ui.panel_conditional("input.func === 'bc'", 
                    ui.input_selectize("bcolor", "Background color", 
                                       ['white', 'black', 'grey']), #'transparent'
                    ui.input_slider("threshold", "Threshold", value=10, min=0, max=20,step=0.5)
            ),
        ),
        ui.panel_main(
            ui.output_plot("image")
        )
    )
)

def server(input, output, session):
    gamma_value = reactive.Value(False)

    @reactive.Effect
    @reactive.event(input.reset)
    def _():
        gamma_value.set(True)
        print('reset')

    @output
    @render.image
    async def image() -> ImgData:
        file_infos: list[FileInfo] = input.file()
        if not file_infos:
            path = f'demo_input/{input.demos()}.png'
            image_data = io.imread(path)
            # raise SilentException()
        else:
            file_info = file_infos[0]
            img = Image.open(file_info["datapath"])
            # Convert to numpy array for skimage processing
            image_data = np.array(img)

        if input.func() == 'invert':
            if input.cspace() == "rgb":
                negative_image = util.invert(image_data)
            elif input.cspace() == "hsl": # OpenCV package
                hsl_image = rgb_to_hsl(image_data)
                negative_image = hsl_image.copy()
                negative_image[:, :, 1] = 1 - negative_image[:, :, 1]
                negative_image = hsl_to_rgb(negative_image)
            elif input.cspace() == "lab":
                lab_image = color.rgb2lab(image_data)
                negative_lab_image = lab_image.copy()
                negative_lab_image[:, :, 0] = 100 - negative_lab_image[:, :, 0] 
                # negative_image = (negative_lab_image * 255).astype(np.uint8)
                negative_image = color.lab2rgb(negative_lab_image)
        elif input.func() == 'bc':
            negative_image = adjust_colors(img_array=image_data, 
                                           color=input.bcolor(),space=input.cspace(),
                                           threshold = input.threshold())

        # print(gamma_value())
        custom_gamma = input.gamma()
        if gamma_value():
            input.reset()
            negative_image = exposure.adjust_gamma(negative_image, gamma=1)
            with reactive.isolate():
                    gamma_value.set(False)
        else:
            negative_image = exposure.adjust_gamma(negative_image, gamma=custom_gamma)                               
        
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
        new_image_np[:height1, :width1] = image_data
        new_image_np[:height2, width1:] = negative_image
        io.imsave("test_results/combin-inverted.png", util.img_as_ubyte(new_image_np))
        return {"src": "test_results/combin-inverted.png", "width": "100%"}


app = App(app_ui, server)
