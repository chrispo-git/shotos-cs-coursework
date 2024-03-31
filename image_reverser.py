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

        for filename in files:
            if filename.endswith(".gif"):
                pil_image = Image.open(f"sprites/{filename}")
                pil_image = pil_image.convert("RGBA")
                data = pil_image.getdata()
                new_img = []
                for item in data:
                    if "F00" in filename: #Ryu
                        if item == (0,0,0,255): #Outline
                            new_img.append((15,56,15,255)) 
                        elif item == (255,255,255,255): #Skin
                            new_img.append((210,226,138,255)) 
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
                    elif "F03" in filename: #Akuma
                        if item == (32,40,64,255): #Clothes
                            new_img.append((63,63,63,255))
                        elif item == (128,80,56,255):#Skin
                            new_img.append((128,80,56,255))
                        elif item == (224,56,48,255): #Hair
                            new_img.append((255,246,183,255))
                        elif item == (25,11,7,255):#Necklace
                            new_img.append((255,204,109,255))
                        else:
                            new_img.append(item)
                    else:
                        new_img.append(item)
                
                pil_image.putdata(new_img)
                pil_image = pil_image.save(f"sprites2/{filename}")
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
                            new_img.append((0,0,0,255)) 
                        elif item == (255,255,255,255): #Skin
                            new_img.append((192,192,192,255)) 
                        else:
                            new_img.append(item)
                    elif "F01" in filename: #Ken
                        if item == (255,0,0,255): #Clothes
                            new_img.append((255,0,220,255))
                        elif item == (240,208,32,255): #Hair
                            new_img.append((255,216,0,255))
                        else:
                            new_img.append(item)
                    elif "F02" in filename: #Sean
                        if item == (135,55,15,255): #Hair (Brown)
                            new_img.append((0,0,0,255))
                        elif item == (247,199,0,255):#Clothes
                            new_img.append((142,142,142,255))
                        elif item == (47,47,47,255): #Belt
                            new_img.append((47,47,47,255))
                        elif item == (183,119,71,255):#Skin
                            new_img.append((181,98,39,255))
                        else:
                            new_img.append(item)
                    elif "F03" in filename: #Akuma
                        if item == (32,40,64,255): #Clothes
                            new_img.append((31,63,40,255))
                        elif item == (128,80,56,255):#Skin
                            new_img.append((128,80,56,255))
                        elif item == (224,56,48,255): #Hair
                            new_img.append((224,56,48,255))
                        elif item == (25,11,7,255):#Necklace
                            new_img.append((25,11,7,255))
                        else:
                            new_img.append(item)
                    else:
                        new_img.append(item)
                
                pil_image.putdata(new_img)
                pil_image = pil_image.save(f"sprites3/{filename}")
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
                            new_img.append((255,106,0,255)) 
                        elif item == (255,255,255,255): #Skin
                            new_img.append((0,0,0,255)) 
                        else:
                            new_img.append(item)
                    elif "F01" in filename: #Ken
                        if item == (255,0,0,255): #Clothes
                            new_img.append((127,201,255,255))
                        elif item == (240,208,32,255): #Hair
                            new_img.append((240,208,32,255))
                        elif item == (255,255,255,255): #Skin
                            new_img.append((102,54,22,255)) 
                        else:
                            new_img.append(item)
                    elif "F02" in filename: #Sean
                        if item == (135,55,15,255): #Hair (Brown)
                            new_img.append((47,47,47,255))
                        elif item == (247,199,0,255):#Clothes
                            new_img.append((41,21,127,255))
                        elif item == (47,47,47,255): #Belt
                            new_img.append((0,0,0,255))
                        elif item == (183,119,71,255):#Skin
                            new_img.append((89,47,17,255))
                        else:
                            new_img.append(item)
                    elif "F03" in filename: #Akuma
                        if item == (32,40,64,255): #Clothes
                            new_img.append((32,40,64,255))
                        elif item == (128,80,56,255):#Skin
                            new_img.append((232,144,104,255))
                        elif item == (224,56,48,255): #Hair
                            new_img.append((64,64,64,255))
                        elif item == (25,11,7,255):#Necklace
                            new_img.append((255,204,109,255))
                        else:
                            new_img.append(item)
                    else:
                        new_img.append(item)
                
                pil_image.putdata(new_img)
                pil_image = pil_image.save(f"sprites4/{filename}")
    for i in ["sprites2","sprites3","sprites4"]:
        for root, dirs, files in os.walk(i):
            #print(files)
            for filename in files:
                if filename.endswith(".gif"):
                    pil_image = Image.open(f"{i}/{filename}")
                    pil_image_flip = pil_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)   
                    pil_image_flip = pil_image_flip.save(f"reverse_{i}/{filename}")