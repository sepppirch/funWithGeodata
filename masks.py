import os
import json
import re
import cv2
from datetime import datetime
import math
#from image_downloading import download_image
#from geotiff import GeoTiff
import numpy as np
#from PIL import Image, ImageFilter


def combineNmapCollisionmap(bigtile):

    name = str(bigtile[0])+"_"+str(bigtile[1])
    src = cv2.imread(name+ '/nmap_small_'+ name +".png",1)
    mask = cv2.imread(name+ '/forest'+ name +".png", 0)
    mask = cv2.resize(mask,(256,256))
    #tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    #_,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)

    b, g, r = cv2.split(src)
    rgba = [b,g,r, mask]
    dst = cv2.merge(rgba,4)

    cv2.imwrite("test.png", dst)



def drawLines(thickness, bigtile, geojson, roadsMask):

    name = str(bigtile[0])+"_"+str(bigtile[1])
    f = open(name+'/'+geojson+name+'.json') #merged
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

                # neighboring pixels
                            for point in range(int(l)*2+1):
                                newPoint = thisP + step * point
                                if newPoint[0] < 2041 and newPoint[0] > 0 and newPoint[1] < 2041 and newPoint[1] > 0 :
                                      

                                    for u in range(thickness):
                                        for v in range(thickness):
                                            px = newPoint[0] + u - int(thickness/2)
                                            py = newPoint[1] + v - int(thickness/2)
                                            #print(str(x) +  "   "+str(y))
                                            if px < 2041 and px > 0 and py < 2041 and py > 0 :


                                                        roadsMask[int(py)][int(px)] = 255
    return roadsMask


def drawLinesRoads(bigtile):

    name = str(bigtile[0])+"_"+str(bigtile[1])
    f = open(name+'/roads_'+name+'.json') #merged
    data = json.load(f)
    roadsMask = np.zeros( (2041,2041,1), dtype=np.uint8)
    for i in data["features"]:
        if "tunnel" in i["properties"]:
             print("skipping tunnel")
        else:
            multi = 1
            col = 64
            if "surface" in i["properties"]:
                 if i["properties"]["surface"] == "asphalt":
                    col = 255                    
            if "highway" in i["properties"]:
                #if i["properties"]["highway"] == "tertiary" or "residential" :
                    #multi = 2
                
                
                onelane = ["tertiary","residential","tertiary_link","secondary_link","private","unclassified"]
                twolane = ["secondary", "primary_link","motorway_link"]
                threelane = ["primary","motorway"]
                if i["properties"]["highway"] in onelane :
                    multi = 2
                    col = 255
                if i["properties"]["highway"] in twolane :
                    multi = 3
                    col = 255
                if i["properties"]["highway"] in threelane :
                    multi = 4
                    col = 255
                
                #if i["properties"]["highway"] == "primary" or "motorway":
                    #multi = 1
            
            thickness = multi  
            #if not "tunnel" in i["properties"].keys() and not "bridge" in i["properties"].keys():
            #if i["properties"]["tunnel"] != "yes" and i["properties"]["bridge"] != "yes":
            for j in range(len(i["geometry"]["coordinates"])-1): #["properties"]
            
                thisP = np.array([i["geometry"]["coordinates"][j][0]  *2041, i["geometry"]["coordinates"][j][1]*2041])
                nextP = np.array([i["geometry"]["coordinates"][j+1][0]  *2041, i["geometry"]["coordinates"][j+1][1]*2041])

                l = np.linalg.norm(thisP - nextP)
            
                step = np.subtract(nextP,thisP)/l/2
                if thisP[0] < 2041 and thisP[0] > 0 and thisP[1] < 2041 and thisP[1] > 0 :
                    if nextP[0] < 2041 and nextP[0] > 0 and nextP[1] < 2041 and nextP[1] > 0 :

                # neighboring pixels
                            for point in range(int(l)*2+1):
                                newPoint = thisP + step * point
                                if newPoint[0] < 2041 and newPoint[0] > 0 and newPoint[1] < 2041 and newPoint[1] > 0 :


                                    for u in range(thickness):
                                        for v in range(thickness):
                                            px = newPoint[0] + u - int(thickness/2)
                                            py = newPoint[1] + v - int(thickness/2)
                                            #print(str(x) +  "   "+str(y))
                                            if px < 2041 and px > 0 and py < 2041 and py > 0 :


                                                        roadsMask[int(py)][int(px)] = col
    cv2.imwrite(name+'/rmask'+name+'.png', roadsMask)


bigtile = (1,-1)
combineNmapCollisionmap(bigtile)
#cv2.imwrite(name+'/teeeeest'+name+'.png', drawLines(2, bigtile, "aerialways_", Mask))
#roadsmask =  drawLinesRoads(bigtile)

'''

riversmask = drawLines(10, bigtile, "rivers_", Mask)
areal = drawLines(6, bigtile, "aerialways_", riversmask)
powerlines = drawLines(5, bigtile, "power_", areal)
buildings = drawLines(5, bigtile, "buildings_", powerlines)
cv2.imwrite(name+'/fmask'+name+'.png', buildings)


Mask = np.zeros( (2041,2041,1), dtype=np.uint8)
areal = drawLines(6, bigtile, "aerialways_", Mask)
powerlines = drawLines(5, bigtile, "power_", areal)

cv2.imshow("ree",powerlines)
cv2.waitKey(0)

# closing all open windows
cv2.destroyAllWindows()'''