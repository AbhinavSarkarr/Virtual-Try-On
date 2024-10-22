from fastapi import FastAPI, Request,BackgroundTasks
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from twilio.rest import Client as TwilioClient
from gradio_client import Client as GradioClient, file
import requests
import os
from PIL import Image
from io import BytesIO
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()


# FastAPI api initialization
app = FastAPI()

# CORS middleware configuration 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Importing private env variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Gradio client configuration
gradio_client = GradioClient("Nymbo/Virtual-Try-On", hf_token="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")
#dict for storing the current user state
user_states = {}

# Cloudinary configuration 
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Function to upload image to Cloudinary and return the URL
def image_to_url(path):
    response = cloudinary.uploader.upload(str(path))
    return response['url']

# Function to process image and provide the resultant image
def process_images(from_number):
    try:
        print("Processing images in the background...")

        # Gradio client call
        result = gradio_client.predict(
            dict={"background": file(user_states[from_number]["images"][0])},
            garm_img=file(user_states[from_number]["images"][1]),
            garment_des="Generic",
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
        )

        print(f"Gradio response: {result}")

        # Upload the result image to Cloudinary
        url = image_to_url(result[0])
        print(f"Generated Cloudinary URL: {url}")

        # Send the result to the user via WhatsApp
        send_whatsapp_message(from_number, url, caption="Here is your Processed Try on Image")

        # Clear user state
        user_states.pop(from_number, None)

    except Exception as e:
        print(f"Error during image processing: {e}")

#Function to send the resultant image expilictly
def send_whatsapp_message(to, image_url, caption="Here is your Processes Try on Image"):
    try:
        print(to)
        print(TWILIO_PHONE_NUMBER)
        message = twilio_client.messages.create(
            body=caption,
            from_=TWILIO_PHONE_NUMBER,
            to=to, 
            media_url=[image_url]
        )
        print(f"Message sent to {to}: {message}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")


# Function to download the image from URL
def download_image(url):
    try:
        response = requests.get(url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))

        original_filename = os.path.basename(url).split('.')[0]  #for dynamic file naming
        filename = f"{original_filename}.jpg"

        rgb_image = image.convert('RGB')  
        rgb_image.save(filename, 'JPEG')
        
        return filename
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")  
    except Exception as e:
        print(f"An error occurred: {e}")  
    return None


# WhatsApp bot endpoint
@app.post('/whatsapp', response_class=PlainTextResponse)
async def whatsapp_bot(request: Request, background_tasks: BackgroundTasks):

    # Get the incoming message details
    form_data = await request.form()
    from_number = form_data.get('From')
    media_urls = form_data.getlist('MediaUrl0')  # Twilio sends images as media

    # Initialize user state if not present
    if from_number not in user_states:
        user_states[from_number] = {"step": 0, "images": []}

    # Handling incoming media
    if media_urls:
        if user_states[from_number]["step"] < 2:

            # Download the image
            img_url = media_urls[0]
            img_path = download_image(img_url)
            if img_path:
                user_states[from_number]["images"].append(img_path)
                user_states[from_number]["step"] += 1

            # Check if both images have been received
            if user_states[from_number]["step"] == 2:
                background_tasks.add_task(process_images, from_number)
                return PlainTextResponse("Images received. Processing the try-on. Please wait...")   
            else:
                return PlainTextResponse("Person's image received. Now, please send the image of the dress.")
        else:
            return PlainTextResponse("You've already sent two images. Please restart the process.")
    else:
        return PlainTextResponse("Please send the Person's image.")


