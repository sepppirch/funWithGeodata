

# Standard imports
import cv2
import numpy as np
from PIL import Image, ImageFilter

import json

# Return the base-2 logarithm of different numbers
def get_contour_areas(contours):
    # returns the areas of all contours as list
    all_areas = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        all_areas.append(area)
    return all_areas




def findThermals(img, sat, dir, fmap, gmap, imap, steepness):
    
    contours = []
    contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contourImg = np.zeros((512,512,3), np.uint8)
    contourImg = sat.copy()#cv2.drawContours(sat, contours, -1, (0,0,255), 1)



    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    #sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    reducedCountures = []
    availability = np.zeros((40,40,1), np.uint8)
    # Iterate over our contours and draw one at a time
    for c in sorted_contours:
        thisfeature = json.loads('{"id": "0", "type": "Feature", "properties": {"name": "thermal", "conf": 100, "rad": 0.0, "multi": 3, "dir":"E"}, "geometry": {"type": "Point", "coordinates": [[0.0, 0.0]]}}')
        csize = cv2.contourArea(c)
        #print(size)

        if csize > 200:
            if csize > 1300:
                csize = 1300

            #print(csize)   
            thisfeature["properties"]["rad"] = (csize)/1000 
            thisfeature["properties"]["dir"] = dir
            #print( thisfeature["properties"])
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            #print(cX,cY)
            thisfeature["geometry"]["coordinates"] = [[cX/512, cY/512]]
            #print(steepness[cX][cY])
            color = (255,0,255)
            if fmap[cX,cY] > 10:
                thisfeature["properties"]["multi"] = 1
                #FOREST
                color = (0,128,0)
            elif gmap[cX,cY] > 10:
                thisfeature["properties"]["multi"] = 2
                #GRASS
                color = (0,255,0)
            elif imap[cX,cY] > 10:
                thisfeature["properties"]["multi"] = 0
                #ICE
                color = (255,0,0)
            


            #if thisfeature["properties"]["multi"] > 0 and thisfeature["properties"]["rad"] > 0.0:
            if availability[int(cX/512*40)][int(cY/512*40)] == 0:
                reducedCountures.append(thisfeature)
                cv2.drawContours(contourImg, [c], -1, (255,0,0), 2)
                cv2.circle(contourImg, (cX, cY), int(csize/50), color, 2)
                availability[int(cX/512*40)][int(cY/512*40)] = 255
            else:
                print("alreadyOccupied")
            
    print(len(reducedCountures))

    return reducedCountures, contourImg

def searchCountures(bigtile):

        name = str(bigtile[0]) + "_" + str(bigtile[1])
        newsize = (512,512)

        nmap =  Image.open(name+"/nmap_small_"+name+".png")
        #

        #fmap =  Image.open(name+"/forest"+name+".png")
        nmap = nmap.resize(newsize, Image.Resampling.BILINEAR)
        nmap = nmap.filter(ImageFilter.BoxBlur(4))
        #print(fmap.getpixel((0,0)))

        fmap = cv2.imread(name+"/forest"+name+".png", cv2.IMREAD_GRAYSCALE)
        fmap = cv2.resize(fmap, (512,512), interpolation = cv2.INTER_LINEAR)
        #cv2.imshow("forest", fmap)
        gmap = cv2.imread(name+"/grass"+name+".png", cv2.IMREAD_GRAYSCALE)
        gmap = cv2.resize(gmap, (512,512), interpolation = cv2.INTER_LINEAR)

        imap = cv2.imread(name+"/ice"+name+".png", cv2.IMREAD_GRAYSCALE)
        imap = cv2.resize(imap, (512,512), interpolation = cv2.INTER_LINEAR)

        sat = cv2.imread(name+"/sat_z12"+name+".jpg")
        sat = cv2.resize(sat, (512,512), interpolation = cv2.INTER_LINEAR)

        grid = Image.open("grid.png")
        grd = grid.getdata()
        #print(fmap[2040,2040])
        #nmap.show()
        red, green, blue = nmap.split()
        # red = steepness(darker = steeper
        # green = East = bright , west dark
        # blue = South = bright
        nmr = red.getdata()
        nmg = green.getdata()
        nmb = blue.getdata()

        newimdataS = []
        newimdataW = []
        newimdataO = []


        i = 0
        for color in nmr:
            s = 190
            # hmd[i] < (17000 + (nmd[i]-140) * 60) -- randomize treeline to avoid a straight line
            if nmr[i] < s and nmb[i] > 128 and nmg[i] > 80 and nmg[i] < 175 and grd[i] == 255:
                #if : 
                newimdataS.append(255)
            
            else:
                newimdataS.append(0)
                
            if nmr[i] < s and nmb[i] > 128 and nmg[i] > 150 and grd[i] == 255: 
                newimdataO.append(255)
            else:
                newimdataO.append(0)

            if nmr[i] < s and nmb[i] > 128 and nmg[i] < 95 and grd[i] == 255: 
                newimdataW.append(255)
            else:
                newimdataW.append(0)
                
            i += 1

        newimS = Image.new('L',newsize)
        newimS.putdata(newimdataS)
        img = np.array(newimS)
        #newimS.show()

        newimW = Image.new('L',newsize)
        newimW.putdata(newimdataW)
        imgW = np.array(newimW)
        #imgW =  cv2.bitwise_not(imgW)

        newimO = Image.new('L',newsize)
        newimO.putdata(newimdataO)
        imgO = np.array(newimO)
        #imgO =  cv2.bitwise_not(imgO)




            




        listS, rimgS = findThermals(img,sat,"S", fmap, gmap, imap, np.array(red))
        #print(listS)
        #cv2.imshow("S", rimgS)

        listW,  rimgW = findThermals(imgW,sat,"W", fmap, gmap, imap, np.array(red))
        #cv2.imshow("W", rimgW)

        listO, rimgO = findThermals(imgO,sat,"O",  fmap, gmap, imap, np.array(red))
        #cv2.imshow("O", rimgO)

        listAll = listS + listO + listW

        outjson = {"type": "FeatureCollection", "features": listAll}
        
        
            

        

        #cv2.waitKey(5000)

            # closing all open windows
        #cv2.destroyAllWindows()

        with open(name +"/thermGen_"+name+".json", "w") as outfile:
            outfile.write(json.dumps(outjson))
        
        

#searchCountures((3,-9))
