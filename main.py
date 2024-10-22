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
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

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
gradio_client = GradioClient("Nymbo/Virtual-Try-On")

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
    try:
        logging.info(f"Uploading image to Cloudinary: {path}")
        response = cloudinary.uploader.upload(str(path))
        logging.info(f"Upload successful, Cloudinary URL: {response['url']}")
        return response['url']
    except Exception as e:
        logging.error(f"Error uploading to Cloudinary: {e}")
        raise e

# Function to process image and provide the resultant image
def process_images(from_number):
    try:
        logging.info(f"Processing images for {from_number} in the background...")

        # Gradio client call
        logging.info("Sending images to Gradio client for processing")
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
        logging.info(f"Gradio response received: {result}")

        # Upload the result image to Cloudinary
        url = image_to_url(result[0])
        logging.info(f"Generated Cloudinary URL: {url}")

        # Send the result to the user via WhatsApp
        send_whatsapp_message(from_number, url, caption="Here is your Processed Try on Image")

        # Clear user state
        logging.info(f"Clearing user state for {from_number}")
        user_states.pop(from_number, None)

    except Exception as e:
        logging.error(f"Error during image processing: {e}")

#Function to send the resultant image expilictly
def send_whatsapp_message(to, image_url, caption="Here is your Processes Try on Image"):
    try:
        logging.info(f"Sending WhatsApp message to {to} with image URL: {image_url}")
        message = twilio_client.messages.create(
            body=caption,
            from_=TWILIO_PHONE_NUMBER,
            to=to, 
            media_url=[image_url]
        )
        logging.info(f"Message sent to {to}: {message.sid}")
    except Exception as e:
        logging.error(f"Error sending WhatsApp message: {e}")


# Function to download the image from URL
def download_image(url):
    try:
        logging.info(f"Downloading image from URL: {url}")
        response = requests.get(url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        original_filename = os.path.basename(url).split('.')[0]  #for dynamic file naming
        filename = f"{original_filename}.jpg"
        rgb_image = image.convert('RGB')  
        rgb_image.save(filename, 'JPEG')
        logging.info(f"Image saved locally as: {filename}")
        return filename
    except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred during image download: {err}")  
    except Exception as e:
        logging.error(f"An error occurred while downloading the image: {e}")  
    return None



# WhatsApp bot endpoint
@app.post('/whatsapp', response_class=PlainTextResponse)
async def whatsapp_bot(request: Request, background_tasks: BackgroundTasks):

    # Get the incoming message details
    form_data = await request.form()
    from_number = form_data.get('From')
    media_urls = form_data.getlist('MediaUrl0')  # Twilio sends images as media
    logging.info(f"Incoming WhatsApp message from {from_number} with media: {media_urls}")

    # Initialize user state if not present
    if from_number not in user_states:
        logging.info(f"Initializing user state for {from_number}")
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
                logging.info(f"Image saved. Step for {from_number} now: {user_states[from_number]['step']}")

            # Check if both images have been received
            if user_states[from_number]["step"] == 2:
                logging.info(f"Both images received for {from_number}, starting background processing.")
                background_tasks.add_task(process_images, from_number)
                return PlainTextResponse("Images received. Processing the try-on. Please wait...")   
            else:
                logging.warning(f"{from_number} already sent two images. Not accepting more.")
                return PlainTextResponse("Person's image received. Now, please send the image of the dress.")
        else:
            return PlainTextResponse("You've already sent two images. Please restart the process.")
    else:
        logging.info(f"No media received from {from_number}.")
        return PlainTextResponse("Please send the Person's image.")
