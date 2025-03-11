# Imports
import streamlit as st
from PIL import Image
from time import sleep
import random
from google import genai
from google.genai import types
import vertexai 
from vertexai.preview.vision_models import ImageGenerationModel
import PIL.Image

gensLeft = 12
missing = []

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
    "proud", "embarrassed", "annoyed", "calm",
    "guilty", "frustrated", "amused", "shy", "relaxed",
    "worried", "anxious", "cheerful", "thoughtful",
    "tired", "relieved", "playful", "silly", "grumpy",
    "curious", "scared", "sleepy", "nervous", "shocked",
    "mad"
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
    global gensLeft
    global missing
    top = Image.open("assets/top.png")
    # Swap background
    getBg(1, 4)
    getBg(2, 4)
    getBg(3, 4)
    while (gensLeft > 0 and len(missing) > 0):
        toGet = missing[0]
        missing.pop(toGet)
        getBg(toGet, 1)


    img1 = Image.open("img/1.png")
    img2 = Image.open("img/2.png")
    img3  =Image.open("img/3.png")

    bg1 = Image.open("img/bg1.png")
    bg2 = Image.open("img/bg2.png")
    bg3  =Image.open("img/bg3.png")

    bg1 = bg1.resize(img1.size)
    bg2 = bg2.resize(img2.size)
    bg3 = bg3.resize(img3.size)

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
def getBg(i, lim):
    global gensLeft
    print("Getting background for "+str(i))
    num = str(i)

    image = PIL.Image.open("img/"+num+".png")

    client = genai.Client(api_key="mmmm no :)")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Create a detailed image generation description that explains what the person or people in the image look like, their clothes, poses, and facial expressions. Pretend they're in front of a landscape from an imaginary far off land that matches their expressions. What does it look like? Describe them and their backgrounds very well.", image])
    print(response.text)

    PROJECT_ID = "chrome-ranger-450123-r5"
    output_file = "img/bg"+num+".png"
    prompt = "Cartooney " + response.text # The text prompt describing what you want to see.

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
    j = 0
    while(j < lim):
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
            person_generation="allow",
        )  
        gensLeft = gensLeft - 1 
        try:
            images[0].save(location=output_file, include_generation_parameters=False)
            print(f"Created output image!")
            j = lim + 1
        except:
            print(f"failed on attempt {i}. Updated prompt to ")
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=["Make this image generator prompt more concise (3/4ths length or less, the background should be an imaginary one to match the person's emotions): " + prompt])
            print(response.text)
            prompt = "Cartooney " + response.text # The text prompt describing what you want to see.
            j = j + 1
            if (j == lim):
                missing.append(i)
    # Optional. View the generated image in a notebook.
    # images[0].show()

    

numPics = 0
takePics()
