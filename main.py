import os.path

import filetype
import pyexiv2
from pathlib import Path

from PIL import Image



def get_metadata_files():
    # assign directory
    directory = '/run/media/bozo/Sante/Foto'
    # iterate over files in
    # that directory
    files = Path(directory).rglob('*')
    xmp_files = []
    exif_files = []
    for filename in files:
        if os.path.isfile(filename):
            # list all the images
            if filetype.is_image(filename):
                # check if image has exif or xmp date
                metadata = pyexiv2.ImageMetadata(str(filename))
                metadata.read()
                if len(metadata.xmp_keys)>0:
                    xmp_files.append(filename)
                if len(metadata.exif_keys):
                    exif_files.append(filename)

            elif filetype.is_video(filename):
                print(f"{filename} is a valid video...")
    return xmp_files


# xmp_files = get_metadata_files()
# print("We're dealing with: {} files!")
# for xmp_file in xmp_files:
#     print(xmp_file)
#     metadata = pyexiv2.ImageMetadata(str(xmp_file))
#     metadata.read()
#     print("-------", xmp_file, "-------")
#     print(metadata.xmp_keys)
#     break



file = "/run/media/bozo/Sante/Foto/Backup/File Nikon100/175NIKON/DSCN1763.JPG"
metadata = pyexiv2.ImageMetadata(str(file))
metadata.read()
print("-------", file, "-------")
print(metadata.xmp_keys)


# if it has xmp convert it to exif

# reorder images trough darktable?