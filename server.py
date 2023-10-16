from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import List
from PIL import Image
from io import BytesIO
import os
from inpaint_image import run_inpaint

app = FastAPI()

# Heartbeat endpoint
@app.get("/heartbeat")
async def heartbeat():
    return {"status": "alive"}

# Endpoint to process the image, prompt, and coordinates
@app.post("/inpaint_image")
async def inpaint_image(
        image: UploadFile = File(...),
        prompt: str = Form(...),
        coordinates: List[List[int]] = Form(...)
):
    try:
        # Validate the image file
        if not image.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Only image files (JPEG/PNG) are allowed.")

        # Process the image here (e.g., call your inpainting function)
        image_bytes = await image.read()
        img = Image.open(BytesIO(image_bytes))

        # Save the uploaded image to a temporary file
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as temp_image_file:
            temp_image_file.write(image_bytes)

        # Call the inpainting function
        inpainted_image_path = run_inpaint(temp_image_path, prompt, coordinates)

        # Read the inpainted image from the returned path
        inpainted_img = Image.open(inpainted_image_path)

        # Convert the inpainted image to bytes
        output_image_bytes = BytesIO()
        inpainted_img.save(output_image_bytes, format="PNG")

        # Clean up the temporary image file
        os.remove(temp_image_path)

        return {
            "image_filename": image.filename,
            "prompt": prompt,
            "coordinates": coordinates,
            "inpainted_image": output_image_bytes.getvalue()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)