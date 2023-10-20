import requests
import base64
# Define your base API URL
BASE_URL = "https://5460-34-82-92-35.ngrok-free.app"  # Replace with your actual base API URL


# Helper image utils
def encode_image(image_path):
    try:
        with open(image_path, "rb") as i:
            b64 = base64.b64encode(i.read())
        return b64.decode("utf-8")
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        return ""

def send_api_request(polygon_coordinates, prompt, uploaded_image_path):
    api_url = f"{BASE_URL}/inpaint_image"
    image = encode_image(uploaded_image_path)

    data = {"image": image,"prompt": prompt, "coordinates": polygon_coordinates}

    try:
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            response_data = response.json()
            image_filename = response_data["image_filename"]
            prompt = response_data["prompt"]
            coordinates = response_data["coordinates"]
            inpainted_image_bytes = response_data["inpainted_image"]

            with open("assets/output.png", "wb") as f:
                f.write(inpainted_image_bytes)
                print("Inpainted image saved as assets/output.png")

            return image_filename, prompt, coordinates
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None

def main():
    # polygon_coordinates = [[100, 100], [800, 100], [800, 800], [100, 800]]
    coordinates = [(100, 100), (300, 100), (300, 300), (100, 300)]
    prompt = "deadpool shooting with guns"
    uploaded_image_path = "assets/sdxl-text2img.png"

    result = send_api_request(coordinates, prompt, uploaded_image_path)
    if result:
        image_filename, prompt, coordinates = result
        print(f"Image Filename: {image_filename}")
        print(f"Prompt: {prompt}")
        print(f"Coordinates: {coordinates}")

if __name__ == "__main__":
    main()