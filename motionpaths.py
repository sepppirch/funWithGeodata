import json
import random
import findConnectedRoads
import cv2
import math
from operator import itemgetter
from fitBezier import reduceToBeziers

def fix(input):
    if input < 0:
        return 0.00000001
    elif input > 0.99999999:
        return 0.9999999
    else:
        return input

#name = "1_-1"

def trafficPaths(prefix, name, max, fclass):
    rawdata = {}
    try:
        f = open(name+'/'+prefix+'_'+name+'.json')
        rawdata = json.load(f)
    except:
        rawdata = {"features":[]}
    #select only motorwas
    if len(rawdata["features"]) > 0:
        selpaths = {"features":[]}
        for i in range (len(rawdata["features"])):
            if rawdata["features"][i]["properties"]["fclass"] in fclass:
                thisfeature =  rawdata["features"][i]
                thisfeature["id"] = i
                selpaths["features"].append(thisfeature)
        

        trains = findConnectedRoads.findJunctions(selpaths)

        if len(trains["features"]) > 0:
        #print(trains["features"][0])
            hmap = cv2.imread(name +'/hmap_burnIn_noRiver_'+name+'.png', cv2.IMREAD_UNCHANGED) #
            hmap = cv2.resize(hmap, (32656,32656), cv2.INTER_CUBIC)

            outdata = {"features":[]}
            ids = []
            for t in range (100):
                start = random.randrange(0, len(trains["features"])-1)


                for i in range(1000):
                    if len(trains["features"][start]["properties"]["lastSegments"]) > 0:
                        start = trains["features"][start]["properties"]["lastSegments"][random.randrange(0, len(trains["features"][start]["properties"]["lastSegments"]))]
                    else:
                        #print(str(start)+ " is first")
                        break

                totlen = 0
                c = 0
                lastP = [0,0,0]
                points={"coordinates":[],"start":start,"len":0.0}


                for i in range(1000):
                    if len(trains["features"][start]["properties"]["nextSegments"]) > 0:
                        totlen = totlen+ float(trains["features"][start]["properties"]["length_3"])
                        #first = True
                        count = 0

                        for p in trains["features"][start]["geometry"]["coordinates"]:
                            if p[0] >= 0 and p[0] < 1 and p[1] >= 0 and p[1] < 1:
                                
                                if trains["features"][start]["properties"]["bridge"] == "T" or trains["features"][start]["properties"]["tunnel"] == "T":
                                    #fcoords = [fix(trains["features"][start]["geometry"]["coordinates"][0][1])*32656, fix(trains["features"][start]["geometry"]["coordinates"][0][0])*32656]
                                    #c = float(hmap[int(fcoords[0])][int(fcoords[1])]*1.5625 - 51200)
                                    
                                    bseg = len(trains["features"][start]["geometry"]["coordinates"]) -1
                                    fcoords = [fix(trains["features"][start]["geometry"]["coordinates"][0][1])*32656, fix(trains["features"][start]["geometry"]["coordinates"][0][0])*32656]
                                    fcoordsL = [fix(trains["features"][start]["geometry"]["coordinates"][bseg][1])*32656, fix(trains["features"][start]["geometry"]["coordinates"][bseg][0])*32656]
                                    c0 = hmap[int(fcoords[0])][int(fcoords[1])]*1.5625 - 51200
                                    clast = hmap[int(fcoordsL[0])][int(fcoordsL[1])]*1.5625 - 51200
                                    step = (clast - c0)/bseg
                                    #print(bseg)
                                    c = c0 + step*count
                                else:
                                    fcoords = [fix(p[1])*32656, fix(p[0])*32656]
                                    c = float(hmap[int(fcoords[0])][int(fcoords[1])]*1.5625 - 51200)
                                    #c = 0
                                thisp = [p[0],p[1],c]
                                    #print(math.dist(thisp, lastP))
                                #if math.dist(thisp, lastP) > 1:
                                points["coordinates"].append(thisp)
                                lastP = thisp
                            count = count + 1   

                        start = trains["features"][start]["properties"]["nextSegments"][random.randrange(0, len(trains["features"][start]["properties"]["nextSegments"]))]
                        
                    else:
                        #print("finished " + str(totlen) + " "+str(len(points["coordinates"])))
                        #print(points)
                        #with open(name +"/cars_"+name+".json",mode="w") as f:
                        points["len"] = totlen
                        if start not in ids:
                            ids.append(start)
                            if len(points["coordinates"]) > 0 and points["len"] > 20000:
                                lpos = len(points["coordinates"])%3
                                if lpos == 1:
                                    points["coordinates"].append(points["coordinates"][len(points["coordinates"])-1])
                                    points["coordinates"].append(points["coordinates"][len(points["coordinates"])-1])
                                elif lpos == 2:
                                    points["coordinates"].append(points["coordinates"][len(points["coordinates"])-1])

                                temp = reduceToBeziers(points["coordinates"])
                                points["coordinates"]=temp
                                outdata["features"].append(points)
                        
                        break


            x = sorted(outdata["features"], key=itemgetter('len'), reverse=True)
            if len(x) > max:
                x = x[:max]
            #for f in x:
                #print(f["len"])
        

            return x
        else:
            return []
    else:
        return []



def pathfromLine(prefix, name):
    f = open(name+'/'+prefix+'_'+name+'.json')
    lines = json.load(f)
    f.close()
    
    #print(lines["features"][0])
    hmap = cv2.imread(name +'/hmap_burnIn_noRiver_'+name+'.png', cv2.IMREAD_UNCHANGED) #
    hmap = cv2.resize(hmap, (32656,32656), cv2.INTER_CUBIC)

    for f in lines["features"]:

            for p in f["geometry"]["coordinates"]:
                fcoords = [fix(p[1])*32656, fix(p[0])*32656]
                c = float(hmap[int(fcoords[0])][int(fcoords[1])]*1.5625 - 51200)
                p.append(c)


    #print(lines)

    with open(name +'/'+prefix+'_spline_'+name+".json",mode="w") as f:
        json.dump(lines,f)








'''

pathfromLine("dam", '2_-4')


 
name = "0_0"
r1 = ["motorway", "motorway_link"]
r2 = ["primary","trunk","secondary","tertiary","unclassified"]
r3 = ["rail"]
data = {"roads1":trafficPaths('roadssmooth',name,5, r1), "roads2":trafficPaths('roadssmooth',name,10, r2), "rail":trafficPaths('rail',name,5, r3)}

with open("F:/CLOUDBASE_git/Content/data/json/cars/cars_X30_y16.json",mode="w") as f:
    json.dump(data,f)
'''    
   
