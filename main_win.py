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




#json_file = open("C:\\Users\\Bozo\\PycharmProjects\\photoReorder\\Desktop.json", "r")
json_file = open("/home/bozo/PycharmProjects/photoReorder/Foto-linux.json", "r")
all_images = json.load(json_file)

for image_file in all_images:
    if not str(image_file).endswith("ico"):
        metadata = pyexiv2.ImageMetadata(str(image_file))
        metadata.read()
        accepted_tags = ["Xmp.xmp.CreateDate", "Xmp.MicrosoftPhoto.DateAcquired", "Exif.Image.DateTime", 'Exif.Photo.DateTimeOriginal', 'Exif.Photo.DateTimeDigitized']
        print("----------------------------------------------")
        print("File: {}".format(image_file))
        file_mod_date = time.strptime(time.ctime(os.path.getmtime(image_file)))
        print("File last date: {}".format(file_mod_date))

        # print("IPTC: ", metadata.iptc_keys)
        # print("EXIF: ", metadata.exif_keys)
        # print("XMP: ", metadata.xmp_keys)

        im = Image.open(image_file)
        exif = im.getexif()
        exif_tags = {ExifTags.TAGS[k]: v for k, v in exif.items() if k in ExifTags.TAGS and type(v) is not bytes}
        if not exif_tags["DateTime"] == '0000:00:00 00:00:00':
            exif_date = time.strptime(exif_tags["DateTime"], "%Y:%m:%d %H:%M:%S")
        else:
            print("Overriding date cause of exif failure!!!")
            exif_override_tag = '0001:01:01 01:01:01'
            exif_date = time.strptime(exif_override_tag, "%Y:%m:%d %H:%M:%S")
        print("File exif date: {}".format(exif_date))
        result = file_mod_date < exif_date
        print("Is exif earlier than file date? {}".format(result))









        # for a in accepted_tags:
        #     if a in metadata.keys():
        #         tag = metadata[a].value
        #
        #
        #         print("\t", a, " : ", tag)



        print("----------------------------------------------")




# Using the timestamp string to create a
# time object/structure
# t_obj = time.strptime(m_ti)

# Transforming the time object to a timestamp
# of ISO 8601 format
# T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)