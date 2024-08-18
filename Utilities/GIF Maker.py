import os
from PIL import Image

# Define input and output directories
input_folder = 'Images'
output_folder = 'GIFs'

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Get all image file names from the input folder
image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

# Sort image files for correct order in GIF
image_files.sort()

# Load images
images = [Image.open(os.path.join(input_folder, img)) for img in image_files]

# Define the output GIF path
output_gif_path = os.path.join(output_folder, 'output.gif')

# Save images as a GIF
images[0].save(
    output_gif_path,
    save_all=True,
    append_images=images[1:], 
    duration=500,  # Duration in milliseconds
    loop=0  # Loop forever
)

print(f'GIF has been saved to {output_gif_path}')
