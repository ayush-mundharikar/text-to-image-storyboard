import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"
}

def generate_image(prompt, style, resolution):
    full_prompt = f"{prompt}, {style} style"

    payload = {
        "inputs": full_prompt,
        "options": {"wait_for_model": True}
    }
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": full_prompt})
    if response.status_code == 200:
        return response.content
    else:
         raise Exception(f"Image generation failed: {response.status_code} - {response.text}")

