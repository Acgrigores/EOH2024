from PIL import Image
import os
import pandas as pd
import numpy as np
from time import sleep
import random
from rembg import remove
from google import genai
from google.genai import types
import vertexai 
from vertexai.preview.vision_models import ImageGenerationModel
import PIL.Image
def collageify():
    top = Image.open("assets/top.png")
    # Swap background
    getBg(1)
    getBg(2)
    getBg(3)

    for i in range(1,4):
        swapbg(Image.open("img/" + str(i) + ".png"),str(i))

    img1 = Image.open("img/1.png")
    img2 = Image.open("img/2.png")
    img3  =Image.open("img/3.png")

    bg1 = Image.open("img/bg1.png")
    bg2 = Image.open("img/bg2.png")
    bg3  =Image.open("img/bg3.png")

    bg1 = bg1.resize(img1.size)
    bg2 = bg2.resize(img2.size)
    bg3 = bg3.resize(img3.size)

    bg1.paste(img1, (0,0), img1)
    bg2.paste(img2, (0,0), img2)
    bg3.paste(img3, (0,0), img3)

    collage = Image.new("RGBA", (img1.width, 3 * img1.height + top.height),(255, 200, 150))
    collage.paste(bg2, (0, img1.height + top.height))
    collage.paste(bg3, (0, 2 * img1.height + top.height))


    # Create and add images to collage
    collage.paste(top, (0,0))
    collage.paste(bg1, (0, top.height))
    collage.paste(bg2, (0, img1.height + top.height))
    collage.paste(bg3, (0, 2 * img1.height + top.height))

    # Save and display collage
    collage.save("img/collage.png")
    st.image(collage)
collageify()