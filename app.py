import numpy as np
from skimage import color, util, io
# import colorsys
from PIL import Image, ImageOps
from shiny import App, render, ui
from shiny.types import FileInfo, ImgData, SilentException
from tohsl import rgb_to_hsl, hsl_to_rgb
from color_change import adjust_colors

app_ui = ui.page_fluid(
    ui.h2("Playing with invert"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_file("file", None, button_label="Upload image",
                # This tells it to accept still photos only (not videos).
                accept="image/*", capture="environment"),
            ui.input_radio_buttons('func', 'Functions',
                    choices = {"invert": "Invert", "bc": "Background color change"}),
            ui.panel_conditional("input.func === 'invert'", 
                    ui.input_radio_buttons("cspace", "Color space",['rgb','hsl','lab'])
                    ),
            ui.panel_conditional("input.func === 'bc'", 
                    ui.input_selectize("bcolor", "Background color", 
                                       ['white', 'black', 'grey']) #'transparent'
            ),
        ),
        ui.panel_main(
            ui.output_plot("image")
        )
    )
)

def server(input, output, session):
    @output
    @render.image
    async def image() -> ImgData:
        file_infos: list[FileInfo] = input.file()
        if not file_infos:
            image_data = io.imread('./oRGB.png')
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
                negative_image[:, :, 2] = 1 - negative_image[:, :, 2]
                negative_image = hsl_to_rgb(negative_image)
            elif input.cspace() == "lab":
                lab_image = color.rgb2lab(image_data)
                negative_lab_image = lab_image.copy()
                negative_lab_image[:, :, 0] = 100 - negative_lab_image[:, :, 0] # range
                # negative_image = (negative_lab_image * 255).astype(np.uint8)
                negative_image = color.lab2rgb(negative_lab_image)
        elif input.func() == 'bc':
            print(image_data[1,1,:])
            negative_image = adjust_colors(image_data, input.bcolor())
            print(image_data[1,1,:])

        # Save for render.image
        io.imsave("small.png", util.img_as_ubyte(negative_image))
        return {"src": "small.png", "width": "100%"}


app = App(app_ui, server)
