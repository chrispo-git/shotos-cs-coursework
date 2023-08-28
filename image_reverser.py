#uses PIL to create a reversed image of all sprites in sprites folder
from PIL import Image, ImageTk
import os

def reverse():
    for root, dirs, files in os.walk("sprites"):
        print(files)
        for filename in files:
            if filename.endswith(".png"):
                pil_image = Image.open(f"sprites/{filename}")
                new_file = f"sprites/{filename}"
                new_file = new_file.replace(".png", ".gif")
                pil_image = pil_image.save(new_file)
    for root, dirs, files in os.walk("sprites"):
        print(files)
        for filename in files:
            if filename.endswith(".gif"):
                pil_image = Image.open(f"sprites/{filename}")
                pil_image_flip = pil_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)   
                pil_image_flip = pil_image_flip.save(f"reverse_sprites/{filename}")