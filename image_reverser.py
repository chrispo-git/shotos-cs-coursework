#uses PIL to create a reversed image of all sprites in sprites folder
from PIL import Image, ImageTk
import os

def reverse():
    for root, dirs, files in os.walk("sprites"):
        #print(files)
        for filename in files:
            if filename.endswith(".png"):
                pil_image = Image.open(f"sprites/{filename}")
                new_file = f"sprites/{filename}"
                new_file = new_file.replace(".png", ".gif")
                pil_image = pil_image.save(new_file)
    for root, dirs, files in os.walk("sprites"):
        #print(files)
        for filename in files:
            if filename.endswith(".gif"):
                pil_image = Image.open(f"sprites/{filename}")
                pil_image_flip = pil_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)   
                pil_image_flip = pil_image_flip.save(f"reverse_sprites/{filename}")
    for root, dirs, files in os.walk("sprites"):
        #print(files)
        for filename in files:
            if filename.endswith(".gif"):
                pil_image = Image.open(f"sprites/{filename}")
                pil_image = pil_image.convert("RGBA")
                data = pil_image.getdata()
                new_img = []
                for item in data:
                    if "F00" in filename: #Ryu
                        if item == (0,0,0,255): #Outline
                            new_img.append((0,34,104,255)) 
                        else:
                            new_img.append(item)
                    elif "F01" in filename: #Ken
                        if item == (255,0,0,255): #Clothes
                            new_img.append((10,22,255,255))
                        elif item == (240,208,32,255): #Hair
                            new_img.append((255,140,0,255))
                        else:
                            new_img.append(item)
                    elif "F02" in filename: #Sean
                        if item == (135,55,15,255): #Hair (Brown)
                            new_img.append((135,55,15,255))
                        elif item == (247,199,0,255):#Clothes
                            new_img.append((152,0,183,255))
                        elif item == (47,47,47,255): #Belt
                            new_img.append((47,47,47,255))
                        elif item == (183,119,71,255):#Skin
                            new_img.append((89,47,17,255))
                        else:
                            new_img.append(item)
                    else:
                        new_img.append(item)
                
                pil_image.putdata(new_img)
                pil_image = pil_image.save(f"sprites2/{filename}")
    for root, dirs, files in os.walk("sprites2"):
        #print(files)
        for filename in files:
            if filename.endswith(".gif"):
                pil_image = Image.open(f"sprites2/{filename}")
                pil_image_flip = pil_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)   
                pil_image_flip = pil_image_flip.save(f"reverse_sprites2/{filename}")