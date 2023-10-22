from setup_inpaint_pipeline import setup_pipeline
from diffusers.utils import load_image
from create_mask import create_mask
from models.base_model import InpaintRequest
from utils.utils import decode_base64_image, encode_image
# width = 1024
# height = 1024

# guidance_scale = 7.5
# num_inference_steps = 30
# inpaint_stength = 0.85

pipe_inpaint = setup_pipeline(base_model_path = "stabilityai/stable-diffusion-xl-base-1.0")

def inpaint_image(inpaint_request: InpaintRequest):
    # Decode the base64-encoded image
    init_image = decode_base64_image(inpaint_request.encoded_image)
    width, height = init_image.size
    mask_image_path = create_mask(width, height, inpaint_request.coordinates)
    mask_image = load_image(mask_image_path)

    image = pipe_inpaint(prompt=inpaint_request.prompt,
                         negative_prompt=inpaint_request.negative_prompt,
                         image=init_image,
                         mask_image=mask_image,
                         strength=inpaint_request.inpaint_strength,
                         guidance_scale=inpaint_request.guidance_scale,
                         num_images_per_prompt=inpaint_request.num_images_per_prompt,
                         num_inference_steps=inpaint_request.num_inference_steps).images[0]

    final_image_path = "output.png"
    image.save(final_image_path)
    return final_image_path

def run_inpaint(inpaint_request: InpaintRequest) -> str:
    final_image_path = inpaint_image(inpaint_request)
    inpainted_image_encoded = encode_image(final_image_path)
    return inpainted_image_encoded


def main():
    # generate mask
    init_image_path = "assets/sdxl-text2img.png"
    prompt = "deadpool shooting with guns"
    coordinates = [(100, 100), (800, 100), (800, 800), (100, 800)]
    # Create an instance of InpaintRequest
    request = InpaintRequest(prompt=prompt, encoded_image=init_image_path, coordinates=coordinates)

    # Call the run_inpaint function with the request
    run_inpaint(request)

if __name__ == "__main__":
    main()