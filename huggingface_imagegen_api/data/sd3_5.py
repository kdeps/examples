import os
import torch
from diffusers import StableDiffusion3Pipeline

# Retrieve the prompt from the environment variable
prompt = os.getenv("PROMPT", "A capybara holding a sign that reads 'Hello World'")

# Remove the file if it already exists
file_path = "/tmp/image.png"
if os.path.exists(file_path):
    os.remove(file_path)

# Load the Stable Diffusion model
pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3.5-large", torch_dtype=torch.bfloat16)
pipe = pipe.to("cuda")

# Generate the image
image = pipe(
    prompt,
    num_inference_steps=28,
    guidance_scale=3.5,
).images[0]

# Save the generated image
image.save(file_path)
