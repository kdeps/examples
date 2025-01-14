import os
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0")

# Retrieve the prompt from the environment variable
prompt = os.getenv("PROMPT", "A capybara holding a sign that reads 'Hello World'")

# Remove the file if it already exists
file_path = "/tmp/image.png"
if os.path.exists(file_path):
    os.remove(file_path)

image = pipe(prompt).images[0]

# Save the generated image
image.save(file_path)
