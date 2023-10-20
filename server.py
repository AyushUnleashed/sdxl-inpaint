from fastapi import FastAPI, Form, HTTPException
from typing import List
from PIL import Image
from io import BytesIO
import os
from pydantic import BaseModel
from inpaint_image import run_inpaint
import base64
app = FastAPI()

# Heartbeat endpoint
@app.get("/heartbeat")
async def heartbeat():
    return {"status": "alive"}
# Endpoint to process the base64-encoded image, prompt, and coordinates

class InpaintRequest(BaseModel):
    image: str
    prompt: str
    coordinates: List[tuple[int, int]]  # Change this line


# Helper image utils
def encode_image(image_path):
    try:
        with open(image_path, "rb") as i:
            b64 = base64.b64encode(i.read())
        return b64.decode("utf-8")
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        return ""


@app.post("/inpaint_image")
async def inpaint_image(request: InpaintRequest):
    try:
        # Decode the base64-encoded image
        img = decode_base64_image(request.image)

        # Save the decoded image to a temporary file
        temp_image_path = "temp_image.jpg"
        img.save(temp_image_path)

        # Call the inpainting function
        inpainted_image_path = run_inpaint(temp_image_path, request.prompt, request.coordinates)

        inpainted_image_encoded = encode_image(inpainted_image_path)
        #
        # # Read the inpainted image from the returned path
        # inpainted_img = Image.open(inpainted_image_path)
        #
        # # Convert the inpainted image to bytes
        # output_image_bytes = BytesIO()
        # inpainted_img.save(output_image_bytes, format="PNG")

        # Clean up the temporary image file
        os.remove(temp_image_path)

        return {
            "prompt": request.prompt,
            "coordinates": request.coordinates,
            "inpainted_image": inpainted_image_encoded
        }

    except Exception as e:
        print(f"Exception occurred with error as {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper to decode input image
def decode_base64_image(image_string):
    base64_image = base64.b64decode(image_string)
    buffer = BytesIO(base64_image)
    image = Image.open(buffer)
    return image

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8125)