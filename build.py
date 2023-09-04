from distutils.core import setup
import py2exe
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

empty_folder(r'dist')
shutil.copytree(r"sprites", r"dist\sprites")
shutil.copytree(r"reverse_sprites", r"dist\reverse_sprites")
shutil.copytree(r"menu", r"dist\menu")
shutil.copytree(r"text", r"dist\text")
shutil.copy(r"default_controls.txt", r"dist\controls.txt")


setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': "main.py"}],
    zipfile = None,
)