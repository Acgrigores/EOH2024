# Imports
import streamlit as st
from PIL import Image
import os
import pandas as pd
import numpy as np
from time import sleep
import random

# App text
st.title('pAInt Me a Picture Photobooth')
explained = st.markdown("*Take three pictures, each with a different emotion; ideas for emotions will be written below, or you can go with your own! Then, an AI will make paintings to match your expressions.*")
emotionTxt = st.markdown("")

# UPDATE THE TEXT TO SHOW EMOTIONS
# Lists of common and then extended emotions to pull from
common_emotions = ["happy", "sad", "angry", "surprised", "afraid"]
extended_emotions = [
    "happy", "sad", "angry", "surprised", "afraid",
    "excited", "bored", "confused", "disappointed", "hopeful",
    "lonely", "proud", "embarrassed", "annoyed", "calm",
    "guilty", "frustrated", "amused", "shy", "relaxed",
    "worried", "loving", "anxious", "cheerful", "thoughtful",
    "tired", "relieved", "playful", "silly", "grumpy",
    "curious", "scared", "sleepy", "nervous", "shocked",
    "mad", "joyful", "confident", "kind", "hopeful"
]
# Function to update emotions
def emoUpdate():
    # Choose a common emotion for the first one
    if numPics == 0:
        rand = random.randint(0,len(common_emotions) - 1)
        emotionTxt.write("***" + common_emotions[rand] + "***")
    # Rarer emotion for numbers 2 and 3
    elif 3 > numPics and numPics > 0:
        rand = random.randint(0,len(extended_emotions) - 1)
        emotionTxt.write("***" + extended_emotions[rand] + "***")

# Runs after you're done taking photos
def afterPhotos():
    emotionTxt.write("**All done!**")
    collageify()

# COMBINE PHOTOS INTO A COLLAGE
def collageify():
    top = Image.open("assets/top.png")
    img1 = Image.open("img/1.png")
    img2 = Image.open("img/2.png")
    img3  =Image.open("img/3.png")
    # Create and add images to collage
    collage = Image.new("RGBA", (img1.width, 3 * img1.height + top.height),(255, 200, 150))
    collage.paste(top, (0,0))
    collage.paste(img1, (0, top.height))
    collage.paste(img2, (0, img1.height + top.height))
    collage.paste(img3, (0, 2 * img1.height + top.height))
    # Save and display collage
    collage.save("img/collage.png")
    st.image(collage)

# TAKE A PHOTO
pics = {}
def takePics():
    global numPics
    if numPics > 2:
        # All done taking pics!
        afterPhotos()
        return
    # Update emotions text
    emoUpdate()
    numPics += 1
    # Add camera
    with st.empty():
        cam = st.camera_input("Camera", key=numPics)
        # Save pic when photo is taken
        if cam:
            img_pil = Image.open(cam)
            img_pil.save(f"img/{numPics}.png")
            st.write("")
            takePics()

numPics = 0
takePics()