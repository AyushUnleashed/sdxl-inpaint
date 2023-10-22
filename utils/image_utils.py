# Helper image utils
import base64
from io import BytesIO
from PIL import Image

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