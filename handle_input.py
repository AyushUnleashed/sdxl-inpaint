import requests
import base64
from io import BytesIO
from PIL import Image

# Base API URL

BASE_URL = "https://452b-34-82-92-35.ngrok-free.app"  # Replace with your actual base API URL


# Helper image utils
def encode_image(image_path):
    try:
        with open(image_path, "rb") as i:
            b64 = base64.b64encode(i.read())
        return b64.decode("utf-8")
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        return ""

# Helper to decode input image
def decode_base64_image(image_string):
    base64_image = base64.b64decode(image_string)
    buffer = BytesIO(base64_image)
    image = Image.open(buffer)
    return image

def send_api_request(polygon_coordinates, prompt, uploaded_image_path):
    api_url = f"{BASE_URL}/inpaint_image"
    image = encode_image(uploaded_image_path)

    data = {"image": image,"prompt": prompt, "coordinates": polygon_coordinates}

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
        # print(f"Image Filename: {image_filename}")
        print(f"Prompt: {prompt}")
        print(f"Coordinates: {coordinates}")

if __name__ == "__main__":
    main()