# WhatsApp Virtual Try-On Bot

A **WhatsApp-based Virtual Try-On Bot** built using **FastAPI**, **Twilio**, **Gradio**, and **Cloudinary**. Users can send images via WhatsApp to virtually try on garments using AI-powered image processing, with results delivered instantly back to their chat.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WhatsApp Virtual Try-On Bot                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   WhatsApp   │    │    Twilio    │    │   FastAPI    │          │
│  │    User      │◄──►│     API      │◄──►│   Backend    │          │
│  └──────────────┘    └──────────────┘    └──────┬───────┘          │
│                                                  │                   │
│                                                  ▼                   │
│                      ┌───────────────────────────────────────┐      │
│                      │         Image Processing Pipeline      │      │
│                      │  ┌─────────────┐    ┌─────────────┐   │      │
│                      │  │   Gradio    │    │ Cloudinary  │   │      │
│                      │  │  Try-On AI  │───►│   Storage   │   │      │
│                      │  └─────────────┘    └─────────────┘   │      │
│                      └───────────────────────────────────────┘      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
Virtual-Try-On/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .env                   # Environment variables (not in repo)
└── README.md              # This file
```

## Author

**Abhinav Sarkar**
- GitHub: [@AbhinavSarkarr](https://github.com/AbhinavSarkarr)
- LinkedIn: [abhinavsarkarrr](https://www.linkedin.com/in/abhinavsarkarrr)
- Portfolio: [abhinav-ai-portfolio.lovable.app](https://abhinav-ai-portfolio.lovable.app/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>Try on clothes virtually through WhatsApp</strong>
</p>


