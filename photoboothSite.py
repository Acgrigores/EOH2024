# Imports
import streamlit as st
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

# REPLACE IMAGE'S BACKGROUND
def swapbg(file, name):
    output = remove(file)
    output.save("img/" + name + ".png")

# COMBINE PHOTOS INTO A COLLAGE
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
def getBg(i):
    print("Getting background for "+str(i))
    num = str(i)

    image = PIL.Image.open("img/"+num+".png")

    client = genai.Client(api_key="in your DREAMS")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Respond with just 3 words describing the moods given by the facial expressions of the person or people pictured here.", image])

    print(response.text)

    PROJECT_ID = "chrome-ranger-450123-r5"
    output_file = "img/bg"+num+".png"
    prompt = "Generate a background image with the following feeling: "+ response.text # The text prompt describing what you want to see.

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

    images = model.generate_images(
        prompt=prompt,
        # Optional parameters
        number_of_images=1,
        language="en",
        # You can't use a seed value and watermark at the same time.
        # add_watermark=False,
        # seed=100,
        aspect_ratio="4:3",
        safety_filter_level="block_some",
        person_generation="dont_allow",
    )
    try:
        images[0].save(location=output_file, include_generation_parameters=False)
        print(f"Created output image")
    except:
        images = model.generate_images(
            prompt=prompt,
            # Optional parameters
            number_of_images=1,
            language="en",
            # You can't use a seed value and watermark at the same time.
            # add_watermark=False,
            # seed=100,
            aspect_ratio="4:3",
            safety_filter_level="block_some",
            person_generation="dont_allow",
        )
        try:
            images[0].save(location=output_file, include_generation_parameters=False)
            print(f"Created output image")
        except:
            print(f"failed :(")
    # Optional. View the generated image in a notebook.
    # images[0].show()

    

numPics = 0
takePics()
