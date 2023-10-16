from setup_inpaint_pipeline import setup_pipeline
from diffusers.utils import load_image
from create_mask import create_mask

# width = 1024
# height = 1024

guidance_scale = 7.5
num_inference_steps = 30
inpaint_stength = 0.85

pipe_inpaint = setup_pipeline(base_model_path = "stabilityai/stable-diffusion-xl-base-1.0")

def inpaint_image(prompt ,init_image_path,mask_image_path,inpaint_request=None):
    init_image = load_image(init_image_path) #.convert("RGB")
    mask_image = load_image(mask_image_path) #.convert("RGB")
    image = pipe_inpaint(prompt=prompt, image=init_image, mask_image=mask_image, strength=inpaint_stength, guidance_scale=guidance_scale,num_images_per_prompt=1,num_inference_steps=num_inference_steps).images[0]
    final_image_path = "output.png"
    image.save(final_image_path)
    return final_image_path

def run_inpaint(init_image_path, prompt, coordinates):
    init_image = load_image(init_image_path)
    width, height = init_image.size
    mask_image_path = create_mask(width, height, coordinates)
    final_image_path = inpaint_image(prompt, init_image_path, mask_image_path)
    return final_image_path


def main():
    # generate mask
    init_image_path = "assets/sdxl-text2img.png"
    prompt = "deadpool shooting with guns"
    coordinates = [(100, 100), (800, 100), (800, 800), (100, 800)]
    run_inpaint(init_image_path, prompt, coordinates)

if __name__ == "__main__":
    main()