import os.path

import filetype
import pyexiv2
from pathlib import Path

from PIL import Image



# assign directory
directory = 'E:\\Foto'

# iterate over files in
# that directory
files = Path(directory).rglob('*')
for filename in files:
    if os.path.isfile(filename):
        # list all the images
        if filetype.is_image(filename):
            # check if image has exif or xmp date
            metadata = pyexiv2.ImageData('test.jpg')
            metadata.read()
            if metadata.xmp_keys():
                print(filename)
            else:
                print("not!!")
        elif filetype.is_video(filename):
            print(f"{filename} is a valid video...")



# if it has xmp convert it to exif

# reorder images trough darktable?