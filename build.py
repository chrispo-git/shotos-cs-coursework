import shutil
import os

def empty_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

empty_folder(r'dist') #Empties the folder so we dont carry anything from prev builds
#Moving all the assets!

os.system("pyinstaller --noconsole main.py")

shutil.copytree(r"sprites", r"dist\main\sprites")
shutil.copytree(r"reverse_sprites", r"dist\main\reverse_sprites")
shutil.copytree(r"sprites2", r"dist\main\sprites2")
shutil.copytree(r"reverse_sprites2", r"dist\main\reverse_sprites2")
shutil.copytree(r"menu", r"dist\main\menu")
shutil.copytree(r"text", r"dist\main\text")
shutil.copy(r"default_controls.txt", r"dist\main\controls.txt")