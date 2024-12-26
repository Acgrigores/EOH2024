# Imports
import streamlit as st
from PIL import Image
import os
import pandas as pd
import numpy as np

# App text
st.title('pAInt me a picture')

# Camera stuff
def takePics():
    images = []
    for i in range(1, 4):
        st.write(f"Capture picture {i}")
        img = st.camera_input(f"Take a photo for image {i}")
        if img:
            # Read image as PIL object
            img_pil = Image.open(img)
            # Save the image to the img folder with the corresponding name
            img_pil.save(f"img/{i}.png")
            images.append(img_pil)
            st.image(img_pil, caption=f"Picture {i}", use_container_width=True)

takePics()