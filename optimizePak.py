import os

#"C:\Program Files\Epic Games\UE_4.27\Engine\Binaries\Win64\UnrealPak.exe" D:\cb_free\WindowsNoEditor\Colab\Content\Paks\Colab-WindowsNoEditor.pak -Extract D:\Extracted

#C:\Users\sebastian>"C:\Program Files\Epic Games\UE_4.27\Engine\Binaries\Win64\UnrealPak.exe" D:\Extracted\Colab-WindowsNoEditor.pak -Create=D:\Extracted\datatopack.txt

#https://www.youtube.com/watch?v=AElxgCRXF64


import shutil 
from shutil import copy, copytree
import json

names = []


with open('S.geojson', 'r') as file:
    data = json.load(file)
    for f in data["features"]:
        n = f["properties"]["name"].split("|")
        names.append(n[1][1:])

print(names)


newfolders = ["buildingsOPT","nwindOPT","owindOPT","swindOPT","riversOPT","roadsOPT","nmapsOPT"]
rootdir = "D:/Extracted/Colab/Content/Maps/alps/bigTest/"

for f in newfolders:
    newpath = rootdir + f
    if not os.path.exists(newpath):
        os.makedirs(newpath)

for n in names:
    '''
    try:
        src_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/buildings/b_" + n +'.uasset'
        destination_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/buildingsOPT/b_" + n +'.uasset'
        copy(src_path, destination_path)

        src_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/buildings/b_" + n +'.uexp'
        destination_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/buildingsOPT/b_" + n +'.uexp'
        copy(src_path, destination_path)
    except:
        print(n)
    try:
        src_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/roads/rw_" + n +'.uasset'
        destination_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/roadsOPT/rw_" + n +'.uasset'
        copy(src_path, destination_path)

        src_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/roads/rw_" + n +'.uexp'
        destination_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/roadsOPT/rw_" + n +'.uexp'
        copy(src_path, destination_path)
    except:
        print(n)
'''
    try:
        src_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/nmaps/n_" + n +'.uasset'
        destination_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/nmapsOPT/n_" + n +'.uasset'
        copy(src_path, destination_path)

        src_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/nmaps/n_" + n +'.uexp'
        destination_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/nmapsOPT/rw_" + n +'.uexp'
        copy(src_path, destination_path)
    except:
        print(n)

    try:
        src_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/rivers/river_" + n +'.uasset'
        destination_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/riversOPT/river_" + n +'.uasset'
        copy(src_path, destination_path)

        src_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/rivers/river_" + n +'.uexp'
        destination_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/riversOPT/river_" + n +'.uexp'
        copy(src_path, destination_path)
    except:
        print(n)
'''
    prefix = ["n","s","o","w"]
    for p in prefix:
        try:
            src_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/"+p+"wind/"+p+"wind__" + n
            destination_path = "D:/Extracted/Colab/Content/Maps/alps/bigTest/"+p+"windOPT/"+p+"wind__" + n
            copytree(src_path, destination_path)
        except:
            print(n)
'''