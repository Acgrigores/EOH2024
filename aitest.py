from google import genai
from google.genai import types
import vertexai 
from vertexai.preview.vision_models import ImageGenerationModel
import PIL.Image
from time import sleep
for i in range(1, 4):

    numInt = i
    num = str(numInt)

    image = PIL.Image.open("img/"+num+".png")

    client = genai.Client(api_key="AIzaSyAREanw-jTADBKqb_Byu_0HCJldjYSI3f8")
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

    images[0].save(location=output_file, include_generation_parameters=False)

    # Optional. View the generated image in a notebook.
    # images[0].show()

    print(f"Created output image")
    sleep(1)
    # Example response:
    # Created output image using 1234567 bytes