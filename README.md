Here’s the updated `README.md` file that includes details about deployment on a DigitalOcean droplet using Docker:

---

# WhatsApp Virtual Try-On Bot

This project is a **WhatsApp-based Virtual Try-On Bot** built using **FastAPI**, **Twilio**, **Gradio**, and **Cloudinary**. The bot allows users to send images via WhatsApp, simulates virtual try-ons using a pre-trained model, and sends the processed image back to the user. The application is deployed on a **DigitalOcean Droplet** using **Docker**.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Deployment with Docker](#deployment-with-docker)
- [Environment Variables](#environment-variables)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [License](#license)

## Features
- **WhatsApp Messaging Integration:** Users can send images directly via WhatsApp using Twilio's API.
- **Virtual Try-On:** Uses a pre-trained Gradio model to process and combine two images (a person’s image and a garment image).
- **Image Processing:** Handles image downloading, saving, and manipulation using the PIL library.
- **Cloudinary Integration:** Uploads processed images to Cloudinary and returns a shareable link to the user.
- **Asynchronous Tasks:** Implements background tasks for image processing, ensuring seamless user interaction.
- **Dockerized Application:** Deployed using Docker for efficient and portable deployment.

## Technologies Used
- **FastAPI**: For the RESTful API.
- **Twilio API**: For WhatsApp messaging services.
- **Gradio Client**: For the virtual try-on image processing using pre-trained models.
- **Cloudinary**: For storing and serving processed images.
- **Pillow (PIL)**: For handling images.
- **dotenv**: For managing environment variables.
- **Docker**: For containerization and deployment on DigitalOcean Droplet.
  
## Installation

### Prerequisites
- Python 3.8+
- Twilio Account with a WhatsApp-enabled number
- Cloudinary Account
- Gradio model (you can use the one you integrated or modify as needed)
- Docker and Docker Compose

### Steps
1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/whatsapp-virtual-try-on.git
    cd whatsapp-virtual-try-on
    ```

2. **Install dependencies:**
    Install all required packages using `pipreqs` or manually:
    ```bash
    pip install -r requirements.txt
    ```

3. **Environment Variables:**
   Create a `.env` file in the root directory and add your credentials:
    ```bash
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_PHONE_NUMBER=your_twilio_whatsapp_number
    CLOUDINARY_CLOUD_NAME=cloudinary://your_cloudinary_credentials
    CLOUDINARY_API_KEY=your_cloudinary_api_key
    CLOUDINARY_API_SECRET=your_cloudinary_api_secret
    ```

4. **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```

5. **Expose your local server (optional):**
   If you're running locally, you can expose your server with a tool like `ngrok`:
    ```bash
    ngrok http 8000
    ```

6. **Configure Twilio Webhook:**
   Set your Twilio WhatsApp sandbox webhook to point to your server:
    ```
    https://your-server-url/whatsapp
    ```

## Deployment with Docker

### DigitalOcean Droplet Setup
1. **Create a DigitalOcean Droplet** with Docker pre-installed or install Docker manually by following [Docker's installation guide](https://docs.docker.com/engine/install/).

2. **Clone your project on the droplet**:
   ```bash
   git clone https://github.com/your-username/whatsapp-virtual-try-on.git
   cd whatsapp-virtual-try-on
   ```

3. **Create a Dockerfile**:
   The `Dockerfile` should look something like this:

   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .

   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

4. **Create a `docker-compose.yml` file** for easy management of containers:
   ```yaml
   version: '3'
   services:
     app:
       build: .
       ports:
         - "8000:8000"
       env_file: .env
   ```

5. **Build and run the Docker container**:
   ```bash
   docker-compose up --build -d
   ```

6. **Access your application**:
   Once the container is running, your application will be available on your droplet’s IP address at port `8000` (or another port if specified).

7. **Set up SSL with Let's Encrypt (Optional but recommended)**:
   Use a reverse proxy (like **Nginx**) and set up SSL using **Let's Encrypt** for secure access to your bot.

### Docker Commands:
- **To rebuild and restart the container**:
  ```bash
  docker-compose up --build -d
  ```

- **To view logs**:
  ```bash
  docker-compose logs
  ```

- **To stop the container**:
  ```bash
  docker-compose down
  ```

## Environment Variables
The following environment variables are required for the project:
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_PHONE_NUMBER=your_twilio_whatsapp_number
    CLOUDINARY_CLOUD_NAME=cloudinary://your_cloudinary_credentials
    CLOUDINARY_API_KEY=your_cloudinary_api_key
    CLOUDINARY_API_SECRET=your_cloudinary_api_secret

Create a `.env` file in your project directory to manage these variables.

## How It Works

1. **User sends images via WhatsApp**:
   - The bot asks the user to send two images: the person’s image and the garment image.

2. **Image Processing**:
   - The bot downloads the images using Twilio’s Media API and stores them temporarily.
   - The Gradio model processes the images to simulate a virtual try-on.

3. **Result Sharing**:
   - The processed image is uploaded to Cloudinary.
   - The bot sends the resulting image back to the user via WhatsApp using Twilio.

## Usage
1. **Send an image of the person** to the WhatsApp number.
2. **Send an image of the garment** you want to try on.
3. The bot will process the images and send you the virtual try-on result!

### Example Interaction:
- User sends: "Here’s the person’s image."
- Bot replies: "Person's image received. Now, please send the image of the dress."
- User sends: "Here’s the dress image."
- Bot replies: "Images received. Processing the try-on. Please wait..."
- After processing, the user receives the processed try-on image.

## Debugging and Logs
- **Log statements** have been added throughout the code to trace image processing steps, API calls, and possible errors. Check the console output for debugging information.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to further modify this `README.md` based on additional features, improvements, or changes in your project!
