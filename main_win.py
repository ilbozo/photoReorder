import json
import os.path
import subprocess, sys
import time
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
                images.append(str(filename))
                im.close()
            except:
                continue
    return images

def write_down():
    all_images = get_images_from_path('E:\\Foto\\Desktop\\')
    json_string = json.dumps(all_images)
    json_file = open("C:\\Users\\Bozo\\PycharmProjects\\photoReorder\\Desktop.json", "w")
    json_file.write(json_string)
    json_file.close()

# write_down()




json_file = open("C:\\Users\\Bozo\\PycharmProjects\\photoReorder\\Desktop.json", "r")
all_images = json.load(json_file)
all_images = ["C:\\Users\\Bozo\\Downloads\\002.JPG"]


#
# command = "Get-FileMetaData {}"
# p = subprocess.Popen(["powershell.exe", command], stdout=sys.stdout)
# p.communicate()


for i in all_images:
    # print(os.stat(i))
    # print(time.ctime(os.path.getatime(i)))
    # print(time.ctime(os.path.getctime(i)))
    # print(time.ctime(os.path.getmtime(i)))
    command = "Get-Item {} | select-object -Property *".format(i)
    p = subprocess.Popen(["powershell.exe", command], stdout=sys.stdout)
    p.communicate()


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




# Using the timestamp string to create a
# time object/structure
# t_obj = time.strptime(m_ti)

# Transforming the time object to a timestamp
# of ISO 8601 format
# T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)