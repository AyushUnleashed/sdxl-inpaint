from pydantic import BaseModel
from typing import List, Tuple


class InpaintRequest(BaseModel):
    prompt: str
    encoded_image: str
    coordinates: List[Tuple[int, int]]
    negative_prompt = "deformed, nsfw, blurr"
    base_model = "stabilityai/stable-diffusion-xl-base-1.0"
    inpaint_strength = 0.85
    num_inference_steps = 30
    guidance_scale = 7.5
    num_images_per_prompt = 1
