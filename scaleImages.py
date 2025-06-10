import cv2
import os

#channels = ["rocks","hmaps","forest","roadsmask"]
channels = ["nmap"]
for ch in channels:
    files = os.listdir("worldmachine/"+ ch)

    #name = "h_X10_Y10.png"
    for name in files:
        filename = "worldmachinequater/"+ch+"/" + name
        hmap = cv2.imread('worldmachine/'+ch+'/'+ name, cv2.IMREAD_UNCHANGED)
        half = cv2.resize(hmap, (512,512), interpolation = cv2.INTER_LINEAR)
        cv2.imwrite(filename, half)