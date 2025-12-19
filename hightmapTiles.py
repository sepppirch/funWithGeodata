import os
import json
import re
import cv2
from datetime import datetime
import math
#from image_downloading import download_image
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
    #tiff_file = "DEM/DEM_NO_austria.tif"
    #tiff_file = "DEM/alps_4258conv.tif"
    #tiff_file = "DEM/DEM_nGermoney1.tif"
    #tiff_file = "Tyrol_5m.tif"
    #tiff_file = "austria_10m.tif"
    geo_tiff = GeoTiff(tiff_file, crs_code=4258)#4258
    array = []
    array = geo_tiff.read_box(area_box)
    hmap = Image.fromarray(np.uint32(array), "I") # or more verbose as Image.fromarray(ar32, 'I')
    #print(hmap.size)
    newsize = (2041, 2041)
    hmap = hmap.resize(newsize, Image.Resampling.BICUBIC)
    newimdata = []
    for color in hmap.getdata():
        newimdata.append(color*10)
    newim = Image.new('I',hmap.size)
    newim.putdata(newimdata)
    #newim.filter(ImageFilter.BoxBlur(10))
    newim.save(name +'/hmap'+name+'.png')
    newim.save(name +'/hmapEU'+name+'.png')
    newim.close()
    
    alt = cv2.imread(name+'/hmap'+name+'.png', cv2.IMREAD_UNCHANGED)
    ksize = (8, 8)


    #ing cv2.blur() method  
    test = cv2.blur(alt, ksize)
    cv2.imwrite(name +'/hmap'+name+'.png', test)
    
    
    
    try:
        #tiff_file = "Tyrol_5m.tif"
        tiff_file = "DEM/Austria_10m4258.tif"
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
        
        try:

            tiff_file = "DEM/Tyrol_5m_4258.tif"
            #tiff_file = "DEM/swiss_2m_ESPG4326.tif"
            geo_tiff = GeoTiff(tiff_file, crs_code=4258, as_crs=4258)#4258
            array = []
            array = geo_tiff.read_box(area_box)
            hmapTy = Image.fromarray(np.uint32(array), "I") 
            print(hmapTy.size)
            print("Tyrol Tile found")
            
            hmapTy = hmapTy.resize(newsize, Image.Resampling.BICUBIC)
            newimgdatTy = []
            newimmaskdataTy = []

            for color in hmapTy.getdata():
                newimgdatTy.append(color*10)
                if color < 1:
                    newimmaskdataTy.append(0)
                else:
                    newimmaskdataTy.append(255)
                
            newimTy = Image.new('I',hmapTy.size)
            newimTy.putdata(newimgdatTy)
            newimTy.save(name+'/hmapTy.png')

            newimmaskTy = Image.new('L',hmapTy.size)
            newimmaskTy.putdata(newimmaskdataTy)
            newimmaskTy.save(name+'/hmapTymask.png')
        
            bg = cv2.imread(name +'/hmap'+name+'.png',cv2.IMREAD_UNCHANGED )
            fg = cv2.imread(name+'/hmapTy.png',cv2.IMREAD_UNCHANGED )
            mask = cv2.imread(name+'/hmapTymask.png',cv2.IMREAD_UNCHANGED )
            #cv2.imshow('fg_mask', mask)
            bg2 = bg.copy() 
            ksize = (10, 10)  
            mask = cv2.blur(mask, ksize)
            #--- Copy pixel values of fg image to bg image wherever the mask is white ---
            bg2[np.where(mask == 255)] = fg[np.where(mask == 255)]
            
            cv2.imwrite(name +'/hmap'+name+'.png', bg2)
        
        except:
            print("tile outside HMAP Tyrol")
        
        
    except:
        print("tile outside HMAP AT")
    



    if os.path.exists(name +'/hmapAT.png'):
        os.remove(name +'/hmapAT.png')
    if os.path.exists(name +'/hmapATmask.png'):
        os.remove(name +'/hmapATmask.png')
    if os.path.exists(name +'/hmapTy.png'):
        os.remove(name +'/hmapTy.png')
    if os.path.exists(name +'/hmapTymask.png'):
        os.remove(name +'/hmapTymask.png')
 

















def subtractRoadMask(bigtile):
    name = str(bigtile[0])+"_"+str(bigtile[1])
    roads = cv2.imread(name+'/roadsmask'+name+'.png', cv2.IMREAD_UNCHANGED)
    lakes = cv2.imread(name+'/lake'+name+'.png', cv2.IMREAD_UNCHANGED)
    lakes = (lakes/256).astype('uint8')
    rivers = cv2.imread(name+'/rivers'+name+'.png', cv2.IMREAD_UNCHANGED)
    rivers = (rivers/256).astype('uint8')
    forest = cv2.imread(name+'/forest'+name+'.png', cv2.IMREAD_UNCHANGED)
    grass = cv2.imread(name+'/grass'+name+'.png', cv2.IMREAD_UNCHANGED)
    rocks = cv2.imread(name+'/rocks'+name+'.png', cv2.IMREAD_UNCHANGED)

    ksize = (2, 2)  
    
    # Using cv2.blur() method  
    roads = roads + lakes
    roads = roads + rivers
    roadsExt = cv2.blur(roads, ksize)
    th, roadsExt = cv2.threshold(roadsExt, 1, 255, cv2.THRESH_BINARY)

    forestSub = cv2.subtract(forest,roadsExt)
    cv2.imwrite(name +'/forest'+name+'.png', forestSub)
    grassSub = cv2.subtract(grass,roadsExt)
    cv2.imwrite(name +'/grass'+name+'.png', grassSub)
    rocks = rocks + roads
    cv2.imwrite(name +'/rocks'+name+'.png', rocks)
















def hightmapBurnIn(bigtile):
    
    tiff_file = "alps_lakes2.tif"
    #tiff_file = "DEM/lakes_eFrance.tif"
    #tiff_file = "DEM/testlake1.tif"
    geo_tiff = GeoTiff(tiff_file, crs_code=4258, as_crs=4258)#4258

    center = (47.48802456352513, 13.233287974359211)
    h=0.1096
    w=0.16
    topLeft = (center[1] + bigtile[1] * w, center[0] - bigtile[0] * h)

    name = str(bigtile[0])+"_"+str(bigtile[1])

    area_box = [(topLeft[0],topLeft[1]), (topLeft[0]+w,topLeft[1]-h)]

    array = geo_tiff.read_box(area_box)
    
    
    hmap = Image.fromarray(np.uint8(array), "RGBA").convert('L') # or more verbose as Image.fromarray(ar32, 'I')
    newsize = (2041, 2041)
    hmap = hmap.resize(newsize, Image.Resampling.BICUBIC)

    newimdata = []
    for color in hmap.getdata():
        newimdata.append(color*256)

    newim = Image.new('I',hmap.size)
    newim.putdata(newimdata)
    newim.save(name +'/lake'+name+'.png')
    newim.close()





    alt = cv2.imread(name+'/hmap'+name+'.png', cv2.IMREAD_UNCHANGED)

    

    lake = cv2.imread(name +'/lake'+name+'.png', cv2.IMREAD_UNCHANGED)
    structure = cv2.imread('struct1.png', cv2.IMREAD_GRAYSCALE)
    print(structure.shape)

    kernel = np.ones((8, 8), np.uint8)
    lake = cv2.erode(lake, kernel) 

    #rivers = cv2.imread(name +'/rivers'+name+'.png', cv2.IMREAD_UNCHANGED)

    roadsMask = np.zeros( (2041,2041,1), dtype=np.uint8 )

    ksize = (5, 5)
    ksize1 = (3, 3)  
    
    # Using cv2.blur() method  
    lakeb = cv2.blur(lake, ksize)  
    lakeb1 = cv2.blur(lake, ksize1)  
   

# Using cv2.erode() method 
    

# Displaying the image 

    # Displaying the image  


    altn = np.copy(alt)
    altm = np.copy(alt)
    altl = np.copy(alt)
    
    ksize = (5,5)

    altb = cv2.blur(altn, ksize) 


    #cv2.imwrite(name+'/overlayed'+name+'.png', alt)

    print("burn in lakes and rivers")

    for x in range(2041):
        for y in range(2041):
            if lakeb[x][y] > 200:
                if (alt[x][y] - lakeb[x][y]/100 - lakeb1[x][y]/100) > 0:
                    altn[x][y] = altn[x][y] - lakeb[x][y]/200 - lakeb1[x][y]/200
                    altl[x][y] = altn[x][y]
                else:
                    altn[x][y] = 0
                    altl[x][y] = 0

    # RIVERS
                                


    f = open(name+'/riversMerged_'+name+'.json') #merged
    data = json.load(f)



    for i in data["features"]:
        #if not "tunnel" in i["properties"].keys() and not "bridge" in i["properties"].keys():
        #if i["properties"]["tunnel"] != "yes" and i["properties"]["bridge"] != "yes":
            for j in range(len(i["geometry"]["coordinates"])-1): #["properties"]

                thisP = np.array([i["geometry"]["coordinates"][j][0]  *2041, i["geometry"]["coordinates"][j][1]*2041])
                nextP = np.array([i["geometry"]["coordinates"][j+1][0]  *2041, i["geometry"]["coordinates"][j+1][1]*2041])
                l = np.linalg.norm(thisP - nextP)
            
                step = np.subtract(nextP,thisP)/l/2


                if thisP[0] < 2041 and thisP[0] > 0 and thisP[1] < 2041 and thisP[1] > 0 :
                    if nextP[0] < 2041 and nextP[0] > 0 and nextP[1] < 2041 and nextP[1] > 0 :
                        cbase =  altl[int(thisP[1])][int(thisP[0])] 
                        cstep = (int(altl[int(nextP[1])][int(nextP[0])]) - int(altl[int(thisP[1])][int(thisP[0])]) ) /l/2
                        if abs(cstep) < 1:
                # neighboring pixels
                            for point in range(int(l)*2+1):

                                newPoint = thisP + step * point

                                if newPoint[0] < 2041 and newPoint[0] > 0 and newPoint[1] < 2041 and newPoint[1] > 0 :
                                    c = altl[int(newPoint[1])][int(newPoint[0])]

                                    for u in range(9):
                                        for v in range(9):
                                            px = newPoint[0] + u - 4
                                            py = newPoint[1] + v - 4
                                            #print(str(x) +  "   "+str(y))
                                            if px < 2041 and px > 0 and py < 2041 and py > 0 :
                                                depression = cbase - 30 + cstep * point
                                                if depression > 0: 
                                                    altn[int(py)][int(px)] = depression
                                                else:
                                                    altn[int(py)][int(px)] = 0
                                                roadsMask[int(py)][int(px)] = 255



    for i in data["features"]:
        #if not "tunnel" in i["properties"].keys() and not "bridge" in i["properties"].keys():
        #if i["properties"]["tunnel"] != "yes" and i["properties"]["bridge"] != "yes":
            for j in range(len(i["geometry"]["coordinates"])-1): #["properties"]

                thisP = np.array([i["geometry"]["coordinates"][j][0]  *2041, i["geometry"]["coordinates"][j][1]*2041])
                nextP = np.array([i["geometry"]["coordinates"][j+1][0]  *2041, i["geometry"]["coordinates"][j+1][1]*2041])
                l = np.linalg.norm(thisP - nextP)
            
                step = np.subtract(nextP,thisP)/l/2


                if thisP[0] < 2041 and thisP[0] > 0 and thisP[1] < 2041 and thisP[1] > 0 :
                    if nextP[0] < 2041 and nextP[0] > 0 and nextP[1] < 2041 and nextP[1] > 0 :
                        cbase =  altl[int(thisP[1])][int(thisP[0])] 
                        cstep = (int(altl[int(nextP[1])][int(nextP[0])]) - int(altl[int(thisP[1])][int(thisP[0])]) ) /l/2
                        if abs(cstep) < 3:
                # neighboring pixels
                            for point in range(int(l)*2+1):

                                newPoint = thisP + step * point

                                if newPoint[0] < 2041 and newPoint[0] > 0 and newPoint[1] < 2041 and newPoint[1] > 0 :
                                    c = altl[int(newPoint[1])][int(newPoint[0])]

                                    for u in range(7):
                                        for v in range(7):
                                            px = newPoint[0] + u - 3
                                            py = newPoint[1] + v - 3
                                            #print(str(x) +  "   "+str(y))
                                            if px < 2041 and px > 0 and py < 2041 and py > 0 :
                                                depression = cbase - 100 + cstep * point
                                                if depression > 0: 
                                                    altn[int(py)][int(px)] = depression
                                                else:
                                                    altn[int(py)][int(px)] = 0                                                    
                                                roadsMask[int(py)][int(px)] = 255


    for i in data["features"]:
        #if not "tunnel" in i["properties"].keys() and not "bridge" in i["properties"].keys():
        #if i["properties"]["tunnel"] != "yes" and i["properties"]["bridge"] != "yes":
            for j in range(len(i["geometry"]["coordinates"])-1): #["properties"]

                thisP = np.array([i["geometry"]["coordinates"][j][0]  *2041, i["geometry"]["coordinates"][j][1]*2041])
                nextP = np.array([i["geometry"]["coordinates"][j+1][0]  *2041, i["geometry"]["coordinates"][j+1][1]*2041])
                l = np.linalg.norm(thisP - nextP)
            
                step = np.subtract(nextP,thisP)/l/2


                if thisP[0] < 2041 and thisP[0] > 0 and thisP[1] < 2041 and thisP[1] > 0 :
                    if nextP[0] < 2041 and nextP[0] > 0 and nextP[1] < 2041 and nextP[1] > 0 :
                        cbase =  altl[int(thisP[1])][int(thisP[0])] 
                        cstep = (int(altl[int(nextP[1])][int(nextP[0])]) - int(altl[int(thisP[1])][int(thisP[0])]) ) /l/2
                        if abs(cstep) < 5:
                # neighboring pixels
                            for point in range(int(l)*2+1):

                                newPoint = thisP + step * point

                                if newPoint[0] < 2041 and newPoint[0] > 0 and newPoint[1] < 2041 and newPoint[1] > 0 :
                                    c = altl[int(newPoint[1])][int(newPoint[0])]
                                
                                    for u in range(5):
                                        for v in range(5):
                                            px = newPoint[0] + u - 2
                                            py = newPoint[1] + v - 2
                                            #print(str(x) +  "   "+str(y))
                                            if px < 2041 and px > 0 and py < 2041 and py > 0 :
                                                depression = cbase - 150 + cstep * point
                                                if depression > 0: 
                                                    altn[int(py)][int(px)] = depression
                                                else:
                                                    altn[int(py)][int(px)] = 0                                                    

                                                roadsMask[int(py)][int(px)] = 255




    for i in data["features"]:
        #if not "tunnel" in i["properties"].keys() and not "bridge" in i["properties"].keys():
        #if i["properties"]["tunnel"] != "yes" and i["properties"]["bridge"] != "yes":
            for j in range(len(i["geometry"]["coordinates"])-1): #["properties"]

                thisP = np.array([i["geometry"]["coordinates"][j][0]  *2041, i["geometry"]["coordinates"][j][1]*2041])
                nextP = np.array([i["geometry"]["coordinates"][j+1][0]  *2041, i["geometry"]["coordinates"][j+1][1]*2041])
                l = np.linalg.norm(thisP - nextP)
            
                step = np.subtract(nextP,thisP)/l/2


                if thisP[0] < 2041 and thisP[0] > 0 and thisP[1] < 2041 and thisP[1] > 0 :
                    if nextP[0] < 2041 and nextP[0] > 0 and nextP[1] < 2041 and nextP[1] > 0 :
                        cbase =  altl[int(thisP[1])][int(thisP[0])] 
                        cstep = (int(altl[int(nextP[1])][int(nextP[0])]) - int(altl[int(thisP[1])][int(thisP[0])]) ) /l/2
                # neighboring pixels
                        for point in range(int(l)*2+1):

                            newPoint = thisP + step * point

                            if newPoint[0] < 2041 and newPoint[0] > 0 and newPoint[1] < 2041 and newPoint[1] > 0 :
                                c = altl[int(newPoint[1])][int(newPoint[0])]

                                for u in range(3):
                                    for v in range(3):
                                        px = newPoint[0] + u - 1
                                        py = newPoint[1] + v - 1
                                        #print(str(x) +  "   "+str(y))
                                        if px < 2041 and px > 0 and py < 2041 and py > 0 :
                                            depression = cbase - 200 + cstep * point
                                            if depression > 0: 
                                                altn[int(py)][int(px)] = depression
                                            else:
                                                altn[int(py)][int(px)] = 0                                                    

                                            roadsMask[int(py)][int(px)] = 255

                        
    

    # B U I L D I N G S
    f = open(name+'/buildings_'+name+'.json')
    data = json.load(f)

    for i in data["features"]:
        p1 = np.array([i["geometry"]["coordinates"][0][0] *2041, i["geometry"]["coordinates"][0][1]*2041])
        if p1[0] < 2041 and p1[0] > 0 and p1[1] < 2041 and p1[1] > 0 :
            c = alt[int(p1[1])][int(p1[0])]
            
            for j in range(len(i["geometry"]["coordinates"])-1): #["properties"]

                thisP = np.array([i["geometry"]["coordinates"][j][0]  *2041, i["geometry"]["coordinates"][j][1]*2041])
                nextP = np.array([i["geometry"]["coordinates"][j+1][0]  *2041, i["geometry"]["coordinates"][j+1][1]*2041])
                l = np.linalg.norm(thisP - nextP)
                if l < 1:
                    l = 1
                step = np.subtract(nextP,thisP)/l/2


                if thisP[0] < 2041 and thisP[0] > 0 and thisP[1] < 2041 and thisP[1] > 0 :
                    if nextP[0] < 2041 and nextP[0] > 0 and nextP[1] < 2041 and nextP[1] > 0 :
                        
                    
                # neighboring pixels
                        for point in range(int(l)*2+1):

                            newPoint = thisP + step * point

                            if newPoint[0] < 2041 and newPoint[0] > 0 and newPoint[1] < 2041 and newPoint[1] > 0 :
                                #roadsMask[int(newPoint[0])][int(newPoint[1])] = 255
                                for u in range(3):
                                    for v in range(3):
                                        px = newPoint[0] + u - 1
                                        py = newPoint[1] + v - 1
                                        #print(str(x) +  "   "+str(y))
                                        if px < 2041 and px > 0 and py < 2041 and py > 0 :
                                                    
                                            altn[int(py)][int(px)] = c
                                            roadsMask[int(py)][int(px)] = 255


    # R O A D S


    f = open(name+'/roads_'+name+'.json')
    data = json.load(f)
    r = open(name+'/rail_'+name+'.json')
    rdata = json.load(r)
    for r in rdata["features"]:
        data["features"].append(r)
        #print(r)
    lanes = 1
    rdep = 0
    Roads3l = ["motorway_link","trunk","primary"]
    Roads2l = ["secondary","unclassified","tertiary","service","rail"]




    for i in data["features"]:

        if not "tunnel" in i["properties"]:
            #print(i)
            i["properties"]["tunnel"] = "F"
        if not "bridge" in i["properties"]:
            i["properties"]["bridge"] = "F"
        if not "highway" in i["properties"]:
            i["properties"]["highway"] = "rail"
        if not "layer" in i["properties"]:
            i["properties"]["layer"] = "0"
        else:
            lvl = 0
            try:
                lvl = float(i["properties"]["layer"])
                #print(lvl)
            except:
                #arr = i["properties"]["layer"].split(";")
                lvl = 0#float(arr[0].replace(",","."))
            i["properties"]["layer"] = lvl
            

        if i["properties"]["tunnel"] == "F" and i["properties"]["bridge"] == "F":

            if i["properties"]["highway"] == "motorway":
                lanes = 5
                #print("highway")
                #print(i["properties"]["highway"])
            elif i["properties"]["highway"] in Roads3l:
                lanes = 4
            elif i["properties"]["highway"] in Roads2l:
                lanes = 3
            else:
                lanes = 2
        #if i["properties"]["tunnel"] != "T" and i["properties"]["bridge"] != "T":

            rdep = float(i["properties"]["layer"]) * -40

            for j in range(len(i["geometry"]["coordinates"])-1): #["properties"]

                thisP = np.array([i["geometry"]["coordinates"][j][0]  *2041, i["geometry"]["coordinates"][j][1]*2041])
                nextP = np.array([i["geometry"]["coordinates"][j+1][0]  *2041, i["geometry"]["coordinates"][j+1][1]*2041])
                l = np.linalg.norm(thisP - nextP)
                #print(l)
                step = np.subtract(nextP,thisP)/l/2


                if thisP[0] < 2041 and thisP[0] > 0 and thisP[1] < 2041 and thisP[1] > 0 :
                    if nextP[0] < 2041 and nextP[0] > 0 and nextP[1] < 2041 and nextP[1] > 0 :
                        cbase =  altb[int(thisP[1])][int(thisP[0])]
                        cstep = (int(altb[int(nextP[1])][int(nextP[0])]) - int(altb[int(thisP[1])][int(thisP[0])]) ) /l/2
                
                        for point in range(int(l)*2+1):

                            newPoint = thisP + step * point

                            if newPoint[0] < 2041 and newPoint[0] > 0 and newPoint[1] < 2041 and newPoint[1] > 0 :
                                c = altb[int(newPoint[1])][int(newPoint[0])]
                    # neighboring pixels 
    

                                if lanes == 1:
                                    altn[int(newPoint[1])][int(newPoint[0])] = cbase + cstep * point - rdep
                                    altm[int(newPoint[1])][int(newPoint[0])] = cbase + cstep * point- rdep
            #roadsMask[int(py)][int(px)] = 255
                                    roadsMask[int(newPoint[1])][int(newPoint[0])] = 255
                                else:

                                    for u in range(lanes):
                                        for v in range(lanes):
                                            px = newPoint[0] + u - int(lanes/2) 
                                            py = newPoint[1] + v - int(lanes/2) 
                                            #print(str(x) +  "   "+str(y))
                                            if px < 2041 and px > 0 and py < 2041 and py > 0 :
                                                        
                                                altn[int(py)][int(px)] = cbase + cstep * point - rdep
                                                altm[int(py)][int(px)] = cbase + cstep * point - rdep
                                                #roadsMask[int(py)][int(px)] = 255

                                                roadsMask[int(py)][int(px)] = 255
                                
                                    
                                    

                                    

            

    #cv2.imwrite(name+'/hmap_burnIn_noRiver'+name+'.png', altn)
    #


    '''
    array = []
    
    tiff_file = "alps_rivers.tif"
    #tiff_file = "DEM/rivers_eFrance.tif"
    geo_tiff = GeoTiff(tiff_file, crs_code=4258, as_crs=4258)#4258
    area_box = [(topLeft[0],topLeft[1]), (topLeft[0]+w,topLeft[1]-h)]
    array = geo_tiff.read_box(area_box)
    
    rivers = Image.fromarray(np.uint8(array), "RGBA").convert('L') # or more verbose as Image.fromarray(ar32, 'I')

    rivers = rivers.resize(newsize, Image.Resampling.BICUBIC)

    newimdata = []

    for color in rivers.getdata():
        newimdata.append(color*256)
    newim = Image.new('I',hmap.size)
    newim.putdata(newimdata)
    newim.save(name +'/rivers'+name+'.png')
    newim.close()
    '''
    # 
    #
    roadsMask = cv2.dilate(roadsMask, (9,9), iterations=1)
    roadsMask =  cv2.blur(roadsMask, (3,3))
    #roadsMask = cv2.threshold(roadsMask, 128, 255, cv2.THRESH_BINARY)

    for x in range(2041):
        for y in range(2041):
            if roadsMask[x][y]  < 10:
                #print(structure[x][y])
                #if altn[x][y] - float(structure[x][y]) *2 > 0:
                altn[x][y] = altn[x][y] + (float(structure[x%256][y%256]) - 120)* 1.1
                #else:
                    #altn[x][y] = 0
                                           
    #
    cv2.imwrite(name+'/roadsmask'+name+'.png', roadsMask)

    altn = cv2.blur(altn, (2,2))
    #altm = cv2.blur(altm, (3,3))
    cv2.imwrite(name+'/hmap_burnIn_'+name+'.png', altn)
    cv2.imwrite(name+'/hmap_burnIn_noRiver_'+name+'.png', altm)
    #cv2.imwrite(name+'/roadsmask'+name+'.png', roadsMask)

def testimage():
    test = np.zeros((2041,2041,1), np.uint16)
    for y in range (50):
        for i in range(2040):
            test[y][i] = math.floor(i*32.12)

    cv2.imwrite('test.png', test)


#hightmapBurnIn((0,-1))
#subtractRoadMask((1,-3))
#testimage()
#makeHightMap((0,-1))