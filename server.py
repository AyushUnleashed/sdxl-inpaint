from fastapi import FastAPI, HTTPException
from inpaint.inpaint_image import run_inpaint
from models.inpaint_request_model import InpaintRequest

app = FastAPI()

# Heartbeat endpoint
@app.get("/heartbeat")
async def heartbeat():
    return {"status": "alive"}

# Inpaint Endpoint
@app.post("/inpaint_image")
async def inpaint_image(base_request: InpaintRequest):
    try:

        # Call the inpainting function
        inpainted_image_encoded = run_inpaint(base_request)

        return {
            "prompt": base_request.prompt,
            "coordinates": base_request.coordinates,
            "inpainted_image": inpainted_image_encoded
        }

    except Exception as e:
        print(f"Exception occurred with error as {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8125)