import json
import random
import findConnectedRoads
import cv2
import math

def fix(input):
    if input < 0:
        return 0.00000001
    elif input > 0.99999999:
        return 0.9999999
    else:
        return input

name = "1_-1"

def trafficPaths(name):

    f = open(name+'/roadssmooth_'+name+'.json')
    rawdata = json.load(f)
    trains = findConnectedRoads.findJunctions(rawdata)
    print(trains["features"][0])
    hmap = cv2.imread(name +'/hmap_burnIn_noRiver_'+name+'.png', cv2.IMREAD_UNCHANGED) #
    hmap = cv2.resize(hmap, (32656,32656), cv2.INTER_CUBIC)


    start = random.randrange(0, len(trains["features"])-1)


    for i in range(100):
        if len(trains["features"][start]["properties"]["lastSegments"]) > 0:
            start = trains["features"][start]["properties"]["lastSegments"][0]
        else:
            print(str(start)+ " is first")
            break

    totlen = 0
    c = 0
    lastP = [0,0,0]
    points={"coordinates":[]}
    for i in range(100):
        if len(trains["features"][start]["properties"]["nextSegments"]) > 0:
            totlen = totlen+ float(trains["features"][start]["properties"]["length_3"])
            #first = True
            for p in trains["features"][start]["geometry"]["coordinates"]:
                if p[0] >= 0 and p[0] < 1 and p[1] >= 0 and p[1] < 1:
                    fcoords = [fix(p[1])*32656, fix(p[0])*32656]
                    if trains["features"][start]["properties"]["bridge"] == "F" and trains["features"][start]["properties"]["tunnel"] == "F":
                        c = float(hmap[int(fcoords[0])][int(fcoords[1])]*1.5625 - 51200)
                    thisp = [p[0],p[1],c]
                        #print(math.dist(thisp, lastP))
                    if math.dist(thisp, lastP) > 1:
                        points["coordinates"].append(thisp)
                        lastP = thisp
                
            start = trains["features"][start]["properties"]["nextSegments"][0]
            
        else:
            print("finished " + str(totlen) + " "+str(len(points["coordinates"])))
            #print(points)
            #with open(name +"/cars_"+name+".json",mode="w") as f:
            with open("F:/CLOUDBASE_git/Content/data/json/cars/cars_X30_y16.json",mode="w") as f:
                json.dump(points,f)
            break



def trainPaths(name):

    f = open(name+'/rail_'+name+'.json')
    rawdata = json.load(f)
    trains = findConnectedRoads.findJunctions(rawdata)
    print(trains["features"][0])
    hmap = cv2.imread(name +'/hmap_burnIn_noRiver_'+name+'.png', cv2.IMREAD_UNCHANGED) #
    hmap = cv2.resize(hmap, (32656,32656), cv2.INTER_CUBIC)


    start = random.randrange(0, len(trains["features"])-1)


    for i in range(100):
        if len(trains["features"][start]["properties"]["lastSegments"]) > 0:
            start = trains["features"][start]["properties"]["lastSegments"][0]
        else:
            print(str(start)+ " is first")
            break

    totlen = 0
    c = 0
    lastP = [0,0,0]
    points={"coordinates":[]}
    for i in range(100):
        if len(trains["features"][start]["properties"]["nextSegments"]) > 0:
            totlen = totlen+ float(trains["features"][start]["properties"]["length_3"])
            #first = True
            for p in trains["features"][start]["geometry"]["coordinates"]:
                if p[0] >= 0 and p[0] < 1 and p[1] >= 0 and p[1] < 1:
                    fcoords = [fix(p[1])*32656, fix(p[0])*32656]
                    if trains["features"][start]["properties"]["bridge"] == "F" and trains["features"][start]["properties"]["tunnel"] == "F":
                        c = float(hmap[int(fcoords[0])][int(fcoords[1])]*1.5625 - 51200)
                    thisp = [p[0],p[1],c]
                        #print(math.dist(thisp, lastP))
                    if math.dist(thisp, lastP) > 1:
                        points["coordinates"].append(thisp)
                        lastP = thisp
                
            start = trains["features"][start]["properties"]["nextSegments"][0]
            
        else:
            print("finished " + str(totlen) + " "+str(len(points["coordinates"])))
            #print(points)
            with open(name +"/trains_"+name+".json",mode="w") as f:
                json.dump(points,f)
            break



def pathfromLine(name):
    f = open(name+'/gletscher_'+name+'.json')
    lines = json.load(f)
    f.close()
    
    print(lines["features"][0])
    hmap = cv2.imread(name +'/hmap_burnIn_noRiver_'+name+'.png', cv2.IMREAD_UNCHANGED) #
    hmap = cv2.resize(hmap, (32656,32656), cv2.INTER_CUBIC)

    for f in lines["features"]:
        for p in f["geometry"]["coordinates"]:
            fcoords = [fix(p[1])*32656, fix(p[0])*32656]
            c = float(hmap[int(fcoords[0])][int(fcoords[1])]*1.5625 - 51200)
            p.append(c) 
    print(lines)

    with open(name +"/gletscher_"+name+".json",mode="w") as f:
        json.dump(lines,f)

#pathfromLine('3_-4')

trafficPaths('0_-1')