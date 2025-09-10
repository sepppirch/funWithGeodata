import cv2
import numpy as np
import os
import glob
import json

image_folder = 'C:/Users/sebastian/Desktop/AI3D/clouds/'
image_paths = glob.glob(os.path.join(image_folder, '*.png')) + glob.glob(os.path.join(image_folder, '*.jpg'))

print("Found images:")
clouds = {"clouds": []}
for path in image_paths:
    name = path.split("\\")[1].split(".")[0]
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    
    blurred = cv2.GaussianBlur(image, (193, 193), 0)
    bigger = cv2.resize(blurred, (7, 7), interpolation=cv2.INTER_CUBIC)
    #cv2.imshow('blurred', blurred)
    #cv2.waitKey()
    cv2.destroyAllWindows()
    pixels = {"name": name, "pixels": []}
    for x in range(7):
        for y in range(7):
            if bigger[x, y][3] > 10:
                z = int(bigger[x, y][3]/50)+1
                for i in range(1,z):
                    p = {"x":x,"y":y,"z":i}
                    pixels["pixels"].append(p)
    clouds["clouds"].append(pixels)
    #print(pixels)
with open("C:/Users/sebastian/Desktop/AI3D/clouds/allclouds.txt", "w") as f:
    json.dump(clouds, f)