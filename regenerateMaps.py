import os
from os.path import exists
from satdl import makeNormalmap, makeRGBHmap
from postprocessHmap import closegaps
import cv2
from PIL import Image

rootdir = os.path.dirname(os.path.realpath(__file__))

def halfscale(path):
   
    #sat = Image.new('RGB', (8192, 8192))
    sat = Image.open(path + "/sat.jpg") 
 
    newsize = (4096, 4096)
    img = sat.resize(newsize, Image.Resampling.BICUBIC)
    img.save(path +'/sat_half.jpg')
    img.close()
# resize image
 

for subdir, dirs, files in os.walk(rootdir):
    #for file in files:
        #print(os.path.join(subdir, file))
    for dir in dirs:
        path = rootdir + "/" + dir 
        file = path + "/height.png"
        if exists(file):
            c = dir.split("_")
            print(dir)
            #halfscale(dir)
            #closegaps(int(c[0]),int(c[1]))
            #makeRGBHmap(path, 8)
            
            makeNormalmap(dir)
