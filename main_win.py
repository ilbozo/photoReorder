import json
import os.path
import datetime
import subprocess, sys
import time
from pathlib import Path
from pprint import pprint

import pyexiv2
from PIL import Image, ExifTags


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
                images.append(str(filename))
                im.close()
            except:
                continue
    return images

def write_down():
    all_images = get_images_from_path('/run/media/bozo/Sante/Foto')
    json_string = json.dumps(all_images)
    json_file = open("/home/bozo/PycharmProjects/photoReorder/Foto-linux.json", "w")
    json_file.write(json_string)
    json_file.close()

#write_down()




json_file = open("/home/bozo/PycharmProjects/photoReorder/Foto-linux.json", "r")
all_images = json.load(json_file)
skip_formats = ["ico", "icns"]

for image_file in all_images:
    for i in skip_formats:
        if not image_file.endswith("." + i):
            print("----------------------------------------------")
            print("File: {}".format(image_file))

            metadata = pyexiv2.ImageMetadata(str(image_file))
            try:
                metadata.read()
                file_mod_date = time.strptime(time.ctime(os.path.getmtime(image_file)))
            except:
                file_mod_date = '2090:01:01 01:01:01'
            print("File last date: {}".format(file_mod_date))

            im = Image.open(image_file)
            exif = im.getexif()
            exif_tags = {ExifTags.TAGS[k]: v for k, v in exif.items() if k in ExifTags.TAGS and type(v) is not bytes}
            if "DateTime" in exif_tags.keys():
                if not exif_tags["DateTime"] == '0000:00:00 00:00:00':
                    print(exif_tags["DateTime"])
                    for sep in [":", "."]:
                        try:
                            exif_date = time.strptime(exif_tags["DateTime"], "%Y{}%m{}%d %H:%M:%S".format(sep, sep))
                        except:
                            exif_date = None
                            continue
                else:
                    print("Overriding date cause of exif failure!!!")
                    exif_override_tag = '0001:01:01 01:01:01'
                    exif_date = time.strptime(exif_override_tag, "%Y:%m:%d %H:%M:%S")
                print("File exif date: {}".format(exif_date))
                result = file_mod_date < exif_date
                print("Is exif earlier than file date? {}".format(result))
            else:
                print("File has no DateTime tag: {}".format(image_file))
                print("Here i should be using the creation date: {}".format(file_mod_date))
            print("\n")


