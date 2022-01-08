import os.path
import time

import filetype
import pyexiv2
from pathlib import Path

from PIL import Image



def get_images_from_path(directory):
    # iterate over files in
    # that directory
    files = Path(directory).rglob('*')
    xmp_files = []
    images = []
    for filename in files:
        if os.path.isfile(filename):
            # list all the images
            try:
                im = Image.open(filename)
                # check if image has exif or xmp date
                images.append(filename)
                im.close()
            except:
                continue
    return images


all_images = get_images_from_path('/run/media/bozo/Sante/export/olympus_c740/0000')

print("\n\n\nWe're dealing with: {} files!\n\n\n".format(len(all_images)))
exif_date = []
other_date = []

for image_file in all_images:
    if not str(image_file).endswith("ico"):
        metadata = pyexiv2.ImageMetadata(str(image_file))
        metadata.read()
        accepted_tags = ["Xmp.xmp.CreateDate", "Xmp.MicrosoftPhoto.DateAcquired", "Exif.Image.DateTime", 'Exif.Photo.DateTimeOriginal', 'Exif.Photo.DateTimeDigitized']
        print("----------------------------------------------")
        print("File: {}".format(image_file))
        print("File creation date: {}", format(time.ctime(os.path.getctime(image_file))))


        print("IPTC: ", metadata.iptc_keys)
        print("EXIF: ", metadata.exif_keys)
        print("XMP: ", metadata.xmp_keys)

        print("Looking for keys and values:")
        for a in accepted_tags:
            if a in metadata.keys():
                print("\t", a, " : ", metadata[a])


        print("----------------------------------------------")





# if it has xmp convert it to exif

# reorder images trough darktable?