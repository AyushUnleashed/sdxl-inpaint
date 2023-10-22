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



#
# class InpaintRequestBuilder:
#     def __init__(self):
#         self._instance = InpaintRequest(
#             prompt="",
#             negative_prompt="",
#             width=0,
#             height=0,
#             coordinates=[(0, 0), (0, 0), (0, 0), (0, 0)],
#             inpaint_stength=0.5,
#             seed=0,
#             guidance_scale=7.5,
#             init_image_path="",
#             mask_image_path="",
#             num_inference_steps=30,
#             num_images_per_prompt=1,
#             base_model="stabilityai/stable-diffusion-xl-base-1.0"
#         )
#
#     def with_prompt(self, prompt: str):
#         self._instance.prompt = prompt
#         return self
#
#     def with_coordinates(self, coordinates: List[Tuple[int, int]]):
#         self._instance.coordinates = coordinates
#         return self
#
#     def with_negative_prompt(self, negative_prompt: str):
#         self._instance.negative_prompt = negative_prompt
#         return self
#
#     def with_width(self, width: int):
#         self._instance.width = width
#         return self
#
#     def with_height(self, height: int):
#         self._instance.height = height
#         return self
#
#     def with_inpaint_strength(self, inpaint_strength: float):
#         self._instance.inpaint_strength = inpaint_strength
#         return self
#
#     def with_seed(self, seed: int):
#         self._instance.seed = seed
#         return self
#
#     def with_num_inference_steps(self, num_inference_steps: int):
#         self._instance.num_inference_steps = num_inference_steps
#         return self
#
#     def with_num_images_per_prompt(self, num_images_per_prompt: int):
#         self._instance.num_images_per_prompt = num_images_per_prompt
#         return self
#
#     def with_base_model(self, base_model: str):
#         self._instance.base_model = base_model
#         return self
#
#     def with_mask_image_path(self, mask_image_path: str):
#         self._instance.mask_image_path = mask_image_path
#         return self
#
#     def with_init_image_path(self, init_image_path: str):
#         self._instance.init_image_path = init_image_path
#         return self
#
#     def build(self):
#         return self._instance
#

# class BaseResponse(BaseModel):
#     images: List[str]
#     nsfw_map: List[bool] = None
