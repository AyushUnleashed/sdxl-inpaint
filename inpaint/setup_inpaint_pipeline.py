import torch
from diffusers import AutoPipelineForText2Image, AutoPipelineForInpainting

device = "cuda"
d_type = torch.float16
torch.cuda.empty_cache()

def setup_pipeline(base_model_path: str):
    pipe_t2i = AutoPipelineForText2Image.from_pretrained(
        base_model_path,
        torch_dtype=d_type, variant="fp16", use_safetensors=True
    ).to(device)

    pipe_inpaint = AutoPipelineForInpainting.from_pipe(pipe_t2i).to(device)
    return pipe_inpaint