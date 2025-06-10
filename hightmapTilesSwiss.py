import os
import json
import re
import cv2
from datetime import datetime
import math
from image_downloading import download_image
from geotiff import GeoTiff
import numpy as np
from PIL import Image, ImageFilter




#center = (47.48802456352513, 13.233287974359211)
#DON'T CHANGE THIS!!!
# https://www.opendem.info/opendemeu_download_4258.html  hightmaps here!!!
def makeHightMap(bigtile):
    center = (47.48802456352513, 13.233287974359211)
    h=0.1096
    w=0.16
    
    topLeft = (center[1] + bigtile[1] * w, center[0] - bigtile[0] * h)
    bottomRight = (topLeft[0]+ w, topLeft[1]- h)
    name = str(bigtile[0])+"_"+str(bigtile[1])
    area_box = [(topLeft[0],topLeft[1]), (topLeft[0]+w,topLeft[1]-h)]

    tiff_file = "DEM/DEM_alps_90m.tif"
    #tiff_file = "DEM/alps_4258conv.tif"
    #tiff_file = "DEM/DEM_E_France.tif"
    #tiff_file = "Tyrol_5m.tif"
    #tiff_file = "austria_10m.tif"
    geo_tiff = GeoTiff(tiff_file, crs_code=4258)#4258
    array = []
    array = geo_tiff.read_box(area_box)
    hmap = Image.fromarray(np.uint32(array), "I") # or more verbose as Image.fromarray(ar32, 'I')
    print(hmap.size)
    newsize = (2041, 2041)
    hmap = hmap.resize(newsize, Image.Resampling.BICUBIC)
    newimdata = []
    for color in hmap.getdata():
        newimdata.append(color*10)
    newim = Image.new('I',hmap.size)
    newim.putdata(newimdata)
    #newim.filter.BoxBlur(3)
    newim.save(name +'/hmap'+name+'.png')
        
    alt = cv2.imread(name+'/hmap'+name+'.png', cv2.IMREAD_UNCHANGED)
    ksize = (8, 8)


    #ing cv2.blur() method  
    test = cv2.blur(alt, ksize)
    cv2.imwrite(name +'/hmap'+name+'.png', test)

    try:

        tiff_file = "DEM/swiss_2m_ESPG4326.tif"
        geo_tiff = GeoTiff(tiff_file, crs_code=4258)#4258
        array = geo_tiff.read_box(area_box)
        hmapAT = Image.fromarray(np.uint32(array), "I") # or more verbose as Image.fromarray(ar32, 'I')
        print(hmapAT.size)
        print("AT Tile found")
        
        hmapAT = hmapAT.resize(newsize, Image.Resampling.BICUBIC)
        newimdataAT = []
        newimmaskdataAT = []


        for color in hmapAT.getdata():
            #print(color)
            newimdataAT.append(color*10)
            if color < 1:
                newimmaskdataAT.append(0)
            else:
                newimmaskdataAT.append(255)

        newimAT = Image.new('I',hmapAT.size)
        newimAT.putdata(newimdataAT)
        newimAT.save(name+'/hmapAT.png')

        newimmask = Image.new('L',hmapAT.size)
        newimmask.putdata(newimmaskdataAT)
        newimmask.save(name+'/hmapATmask.png')

        bg = cv2.imread(name +'/hmap'+name+'.png',cv2.IMREAD_UNCHANGED )
        fg = cv2.imread(name+'/hmapAT.png',cv2.IMREAD_UNCHANGED )
        mask = cv2.imread(name+'/hmapATmask.png',cv2.IMREAD_UNCHANGED )

        bg2 = bg.copy() 
        ksize = (10, 10)  
        mask = cv2.blur(mask, ksize)
        #--- Copy pixel values of fg image to bg image wherever the mask is white ---
        bg2[np.where(mask == 255)] = fg[np.where(mask == 255)]
        
        cv2.imwrite(name +'/hmap'+name+'.png', bg2)
        
    except:
        print("tile outside HMAP SWISS")




    if os.path.exists(name +'/hmapAT.png'):
        os.remove(name +'/hmapAT.png')
    if os.path.exists(name +'/hmapATmask.png'):
        os.remove(name +'/hmapATmask.png')
    if os.path.exists(name +'/hmapTy.png'):
        os.remove(name +'/hmapTy.png')


#makeHightMap((10,1))
