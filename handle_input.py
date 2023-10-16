import requests

# Define your base API URL
BASE_URL = "http://localhost:8125"  # Replace with your actual base API URL

def send_api_request(polygon_coordinates, prompt, uploaded_image_path):
    api_url = f"{BASE_URL}/inpaint_image"

    files = {"image": ("image.jpg", open(uploaded_image_path, "rb"), "image/jpeg")}
    data = {"prompt": prompt, "coordinates": polygon_coordinates}

    try:
        response = requests.post(api_url, files=files, data=data)

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
    polygon_coordinates = [[100, 100], [200, 100], [200, 200], [100, 200]]
    prompt = "Inpaint the specified area."
    uploaded_image_path = "your_image.jpg"

    result = send_api_request(polygon_coordinates, prompt, uploaded_image_path)
    if result:
        image_filename, prompt, coordinates = result
        print(f"Image Filename: {image_filename}")
        print(f"Prompt: {prompt}")
        print(f"Coordinates: {coordinates}")

if __name__ == "__main__":
    main()