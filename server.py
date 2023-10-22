from fastapi import FastAPI, HTTPException
from utils.utils import encode_image
from inpaint_image import run_inpaint

app = FastAPI()

# Heartbeat endpoint
@app.get("/heartbeat")
async def heartbeat():
    return {"status": "alive"}
# Endpoint to process the base64-encoded image, prompt, and coordinates


from models.base_model import InpaintRequest

# class InpaintRequest(BaseModel):
#     image: str
#     prompt: str
#     coordinates: List[Tuple[int, int]]  # Change this line
#


@app.post("/inpaint_image")
async def inpaint_image(base_request: InpaintRequest):
    try:

        # Check if required fields are provided
        if not base_request.prompt or not base_request.encoded_image or not base_request.coordinates:
            raise HTTPException(status_code=400, detail="Required fields are missing in the request.")

        # Create an InpaintRequest object with values from the base_request
        inpaint_request = base_request.copy(deep=True)

        print(f"This is the inpaint request:\n {inpaint_request}")
        print(f"\n\nThis is the base request:\n {base_request}")

        # Call the inpainting function
        inpainted_image_encoded = run_inpaint(inpaint_request)


        return {
            "prompt": inpaint_request.prompt,
            "coordinates": inpaint_request.coordinates,
            "inpainted_image": inpainted_image_encoded
        }

    except Exception as e:
        print(f"Exception occurred with error as {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8125)