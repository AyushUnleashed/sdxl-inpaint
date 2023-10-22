import requests
import os
from dotenv import load_dotenv
from utils.utils import decode_base64_image, encode_image

# Load environment variables from the .env file
load_dotenv()

# Base API URL
BASE_URL = os.getenv("BASE_URL") or ""

SD_15 = "runwayml/stable-diffusion-v1-5"
SD_21 = "stabilityai/stable-diffusion-2"
SD_XL = "stabilityai/stable-diffusion-xl-base-1.0"

def send_api_request(polygon_coordinates, prompt, uploaded_image_path):
    api_url = f"{BASE_URL}/inpaint_image"
    encoded_image= encode_image(uploaded_image_path)

    data = {"encoded_image": encoded_image,"prompt": prompt, "coordinates": polygon_coordinates,"base_model": SD_15}

    try:
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            response_data = response.json()
            # image_filename = response_data["image_filename"]
            prompt = response_data["prompt"]
            coordinates = response_data["coordinates"]
            inpainted_image_pil = decode_base64_image(response_data["inpainted_image"])
            inpainted_image_pil.save("assets/server_output.png")

            return inpainted_image_pil, prompt, coordinates
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None

def main():
    # polygon_coordinates = [[100, 100], [800, 100], [800, 800], [100, 800]]
    polygon_coordinates = [[100, 100], [300, 100], [800, 200], [100, 800]]
    prompt = "deadpool shooting with guns"
    uploaded_image_path = "assets/sdxl-text2img.png"

    result = send_api_request(polygon_coordinates, prompt, uploaded_image_path)
    if result:
        inpainted_image, prompt, coordinates = result
        print(f"Prompt: {prompt}")
        print(f"Coordinates: {coordinates}")

if __name__ == "__main__":
    main()