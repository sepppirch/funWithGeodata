import cv2
import json
import numpy as np
import findConnectedRoads
import copy
import earclipping
import overpassQuery
import os
import os.path
import shutil 
from shutil import copy as cp

def ccw(A,B,C):
	return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def intersectionPoint(p1_start,p1_end,p2_start,p2_end):

    p = np.asarray(p1_start)
    r = ( np.asarray(p1_end)- np.asarray(p1_start))

    q =  np.asarray(p2_start)
    s  = ( np.asarray(p2_end)- np.asarray(p2_start))

    t = np.cross(q - p,s)/(np.cross(r,s))

    # This is the intersection point
    i = p + t*r

    return i

def findIntersectionPoint(p1_start,p1_end):
    border1 = [[0,0],[0,1]]
    border2 = [[0,0],[1,0]]
    border3 = [[1,0],[1,1]]
    border4 = [[0,1],[1,1]]
    if intersect(border1[0],border1[1], p1_start,p1_end):
        return(intersectionPoint(border1[0],border1[1], p1_start,p1_end))
    if intersect(border2[0],border2[1], p1_start,p1_end):
        return(intersectionPoint(border2[0],border2[1], p1_start,p1_end))
    if intersect(border3[0],border3[1], p1_start,p1_end):
        return(intersectionPoint(border3[0],border3[1], p1_start,p1_end))
    if intersect(border4[0],border4[1], p1_start,p1_end):
        return(intersectionPoint(border4[0],border4[1], p1_start,p1_end))


name = "0_0"


    


def makeLakes(name):
    size = 204000
    verts = []
    UVs = []
    tris = []

    rwidth = 0.005
    outfile = {}
    outfile["lakes"] = []
    
    hmap = cv2.imread(name +'/hmap'+name+'.png', cv2.IMREAD_UNCHANGED)
    f = open(name+'/lakes_'+name+'.json')
    data = json.load(f)
    #if len(data["features"])>0 :
    for sample in data["features"]:
        xmin = 1
        ymin = 1
        xmax = 0
        ymax = 0
        w = 0
        h = 0
        midpoint = [0,0,0]
        p1 =  sample["geometry"]["coordinates"][0]
        if p1[0] < 1 and p1[0] > 0 and p1[1] < 1 and p1[1] > 0 :
            for p in sample["geometry"]["coordinates"]:
                #print(p)
                if p[0] > xmax:
                    xmax = p[0]
                if p[1] > ymax:
                    ymax = p[1]
                if p[0] < xmin:
                    xmin = p[0]
                if p[1] < ymin:
                    ymin = p[1]
            w = xmax - xmin
            h = ymax - ymin
            z = hmap[int(p1[1]*2040)][int(p1[0]*2040)]*1.5625 - 51200
        # p1 --- p2
        # p3 --- p4
            p1 =[xmin*size, ymax*size, z]
            p2 =[xmax*size, ymax*size, z]
            p3 =[xmin*size, ymin*size, z]
            p4 =[xmax*size, ymin*size, z]
            t1 = [2,1,3]
            t2 = [3,4,2]
            midpoint = [(xmin + w/2)*size , (ymin + h/2)*size , z]
            print(str(midpoint) + ' ' + str(w*size) + " " + str(h*size))
            thislake = {}
            thislake["p"] = midpoint
            thislake["w"] = w
            thislake["h"] = h

            outfile["lakes"].append(thislake)     
        else:
            print("skip")
    print(outfile)
    json_object = json.dumps(outfile)

    #writing to sample.json
    with open(name+"/lakesReady_"+ name+".json", "w") as outfile:
        outfile.write(json_object)
    #else:
        #print("empty")






def makeLakesMesh(name):
    size = 204000
    verts = []
    tris = []

    rwidth = 0.005
    outfile = {}
    outfile["lakes"] = []
    
    hmap = cv2.imread(name +'/hmap'+name+'.png', cv2.IMREAD_UNCHANGED)
    f = open(name+'/lakes_'+name+'.json')
    data = json.load(f)
    #if len(data["features"])>0 :
    contours = []
    altis = []
    for sample in data["features"]:
        z = 0
        midpoint = [0,0,0]
        p1 =  sample["geometry"]["coordinates"][0]
        if p1[0] < 1 and p1[0] > 0 and p1[1] < 1 and p1[1] > 0 :
            #print("newcountur")
            newcountur = []
            count = 0
            thissample = earclipping.findLoopDir(sample["geometry"]["coordinates"])
            for p in thissample:
                #count = (count +1)%6
                #if count == 0:
                newcountur.append([p[0]*size,p[1]*size])
                #print(p)

            z = hmap[int(p1[1]*2040)][int(p1[0]*2040)]*1.5625 - 51200
            altis.append(z)
            print(z)
            contours.append(newcountur)
     
        else:
            print("skip")

    
    triangles = []
    offset = 0
    print(str(len(contours)))
    print(altis)
    #contours = [contours[1] ]
    ac = 0
    for c in contours:
        
        try:
            tris = earclipping.clipEars(c)
            for t in tris:
                triangles.append([t[0]+offset,t[1]+offset,t[2]+offset])
           
            for p in c:
                verts.append([p[0],p[1],altis[ac]])
            
            offset = len(verts)
            print("success")
            ac+=1
            print(ac)
        except:
            print("Failed earclipping " + str(len(c)))
        
    open(name +'/lakes_'+name+'.obj', 'w').close()
    with open(name +'/lakes_'+name+'.obj', 'a') as f1:
        for v in verts:
            line = "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + '\n'
            f1.write(line)
        
        for v in verts:
            line = "vt " + str(v[0]) + " " + str(v[1]) +'\n'
            f1.write(line)
        
        #for i in range(len(tris)):
            #f1.write('\ng wall'+str(i)+'\nusemtl water'+str(i)+'\n')
        for t in triangles:
                #print(t)
                line = "f " + str(t[0] +1)+"/" +str(t[0] +1)+ " " +str(t[1] +1)+"/" +str(t[1] +1) + " "+ str(t[2] +1)+"/" +str(t[2] +1) + '\n'
                f1.write(line)

#makeLakesMesh("2_-4")








def fix(input):
    if input < 0:
        return 0.00000001
    elif input > 0.99999999:
        return 0.9999999
    else:
        return input







def makeRiverMesh(name):

    size = 204000
    verts = []
    UVs = []
    tris = []

    rwidth = 0.003
    # Rivers
    hmap = cv2.imread(name +'/hmap'+name+'.png', cv2.IMREAD_UNCHANGED)
    hmap = cv2.resize(hmap, (32656,32656), cv2.INTER_CUBIC)
    lakes = cv2.imread(name+'/lake'+name+'.png', cv2.IMREAD_UNCHANGED)
    lakes = (lakes/256).astype('uint8')

    f = open(name+'/riversMerged_'+name+'.json')
    data = json.load(f)

    segments = []

    #if len(data["features"])>0 :

        # first, cut segments at tile borders
    for sample in data["features"]:
        isInside = False
        p = sample["geometry"]["coordinates"][0]
        thisSegment = {}
        thisSegment["coordinates"] = []

        lastP = [0,0]

        

        if p[0] < 1 and p[0] > 0 and p[1] < 1 and p[1] > 0 :

            isInside = True

        count = 0
        for p in sample["geometry"]["coordinates"]:
            count += 1
            if p[0] < 1 and p[0] > 0 and p[1] < 1 and p[1] > 0 :
                
                if not isInside:
                    #print("firstpoint inside")
                    isInside = True
                    ip = findIntersectionPoint(lastP,p)
                    x = [ip[0],ip[1],0]
                    print(ip)
                    try:
                        thisSegment["coordinates"].append(x)
                    except:
                        print("error")
                    #print(x)
                thisSegment["coordinates"].append([p[0],p[1],0])
                #print(p)

            else:
                if isInside:
                    ip = findIntersectionPoint(lastP,p)
                    x = [ip[0],ip[1],0] 
                    thisSegment["coordinates"].append(x)
                    segments.append(thisSegment)
                    thisSegment = {}
                    thisSegment["coordinates"] = []
                    isInside = False
                    #print(p)
                #print("outside")
            if count == len(p):
                segments.append(thisSegment)
            lastP = p

    #print(segments)

    for s in segments:
        totalLength = 0
    #s = segments[1]
        vl = len(verts)
        
        for i in range(len(s["coordinates"])):
            lastvalidc = 0
            if i > 0:
                AB = np.subtract(s["coordinates"][i-1], s["coordinates"][i])
                length = np.linalg.norm(AB)
                totalLength += length
                n1 = ([AB[1]*-1, AB[0],0]/length) * rwidth
                n2 = n1 *-1
                n12 = n1
                n22 = n2
                if i < len(s["coordinates"])-1:
                    BC = np.subtract(s["coordinates"][i], s["coordinates"][i+1])
                    length2 = np.linalg.norm(BC)
                    n12 = ([BC[1]*-1, BC[0],0]/length2) * rwidth
                    n22 = n12 *-1

                na = (n1+n12)/2
                nb = (n2+n22)/2


                lakeoffset = 0

                fcoords = [fix(s["coordinates"][i][1])*2041, fix(s["coordinates"][i][0])*2041]
                if lakes[int(fcoords[0])][int(fcoords[1])] > 1:
                    lakeoffset = 100


                if i == 1:
                                    # get Z coordinate from hightmap
                    fcoords = [fix(s["coordinates"][i-1][1])*32656, fix(s["coordinates"][i-1][0])*32656]   
                    c = hmap[int(fcoords[0])][int(fcoords[1])]*1.5625 - 51200
                    lastvalidc = c
                    p0 = (s["coordinates"][i-1]+na) * size
                    p1 = (s["coordinates"][i-1]+nb ) * size
                    verts.append([p0[0],p0[1],c-lakeoffset])
                    verts.append([p1[0],p1[1],c-lakeoffset])
                    UVs.append([0,0])
                    UVs.append([0,1])

                                                    # get Z coordinate from hightmap

                fcoords = [fix(s["coordinates"][i][1])*32656, fix(s["coordinates"][i][0])*32656]
                c = hmap[int(fcoords[0])][int(fcoords[1])]*1.5625 - 51200

                #g = hmap[int(s["coordinates"][i-1][1]*2040)][int(s["coordinates"][i-1][0]*2040)]*1.5625 - 51200
                '''
                dif = c-lastvalidc
                if dif <= 0:
                    lastvalidc = c
                else:
                    c = lastvalidc

                '''

                #print(c)

                p0 = (s["coordinates"][i]+na)* size
                p1 = (s["coordinates"][i]+nb)* size
                verts.append([p0[0],p0[1],c-lakeoffset])
                verts.append([p1[0],p1[1],c-lakeoffset])
                UVs.append([totalLength * 100,0])
                UVs.append([totalLength * 100,1])
                
            if i < (len(s["coordinates"])-1):
                    t1 = [2 + i*2 + vl, 1 + i*2 + vl, 3 + i*2 + vl]
                    t2 = [3 + i*2 + vl, 4 + i*2 + vl, 2 + i*2 + vl]
                    tris.append(t1)
                    tris.append(t2)

        #print(np.linalg.norm(AB)*1000)
    #print("---------------")

    #print(intersect([-1,   0.5],[1,   0.5],[0,    0],[0,    1]))

    #print(verts)

    open(name +'/rivers_'+name+'.obj', 'w').close()
    with open(name +'/rivers_'+name+'.obj', 'a') as f1:
        for v in verts:
            line = "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + '\n'
            f1.write(line)

        for u in UVs:
            line = "vt " + str(u[0]) + " " + str(u[1]) +'\n'
            f1.write(line)

        for t in tris:
        # line = "f " + str(t[0]) + " "+ str(t[1])  +" "+ str(t[2])  + '\n'
            line = "f " + str(t[0]) + "/" + str(t[0]) + " "+ str(t[1]) + "/" +str(t[1]) +" "+ str(t[2]) + "/"+ str(t[2]) + '\n'

            f1.write(line)
    #else:
        #print("empty")






















def makeRoadMesh(bigtile):
    name = str(bigtile[0])+"_"+str(bigtile[1])
    size = 204000
    verts = []
    UVs = []
    tris3Lane = []
    tris2Lane = []
    tris1Lane = []
    trisRail = []
    tris = []
    lanes = 0
    rwidth = 0.0008
    depth = 10
    hmap = cv2.imread(name +'/hmap_burnIn_noRiver_'+name+'.png', cv2.IMREAD_UNCHANGED) #
    ksize = (5, 5)
    hmap = cv2.resize(hmap, (32656,32656), cv2.INTER_CUBIC)

    #ing cv2.blur() method  
    #hmap = cv2.GaussianBlur(hmap, ksize,cv2.BORDER_DEFAULT)
    #print(hmap.shape)
    InstancedMeshBridges = {}
    InstancedMeshBridges["features"] = []
    f = open(name+'/roadssmooth_'+name+'.json')
    rawdata = json.load(f)

    r = open(name+'/rail_'+name+'.json')
    rdata = json.load(r)
    for r in rdata["features"]:
        rawdata["features"].append(r)

    lanes3 = ["motorway","motorway_link"]
    lanes2 = ["primary","trunk","secondary"]
#3 lanes
    roads = {"type": "FeatureCollection", "features": []}
    bridges = {"type": "FeatureCollection", "features": []}
    tunnels = {"type": "FeatureCollection", "features": []}
# 2Lanes
    roads2 = {"type": "FeatureCollection", "features": []}
    bridges2 = {"type": "FeatureCollection", "features": []}
# 1 Lane
    roads1 = {"type": "FeatureCollection", "features": []}
    bridges1 = {"type": "FeatureCollection", "features": []}
# RAIL
    roadsR = {"type": "FeatureCollection", "features": []}
    bridgesR = {"type": "FeatureCollection", "features": []}
    #print("xxx")
    #print(len(rawdata["features"]))
    for s in rawdata["features"]:
            
            if s["properties"]["tunnel"] == "T":
                t = {"coordinates":s["geometry"]["coordinates"], "bridge":0, "tunnel":1}
                tunnels["features"].append(t)
            elif s["properties"]["fclass"] in lanes3 :
                if s["properties"]["bridge"] == "T" : #or s["properties"]["tunnel"] == "T"
                    bridges["features"].append(s)
                else:
                    roads["features"].append(s)
            elif s["properties"]["fclass"] in lanes2:
                if s["properties"]["bridge"] == "T" :
                    bridges2["features"].append(s)
                else:
                    roads2["features"].append(s)
            elif s["properties"]["fclass"] == "rail":
                if s["properties"]["bridge"] == "T" :
                    bridgesR["features"].append(s)
                else:
                    roadsR["features"].append(s)

            else:
                if s["properties"]["bridge"] == "T" :
                    bridges1["features"].append(s)
                else:
                    roads1["features"].append(s)

    #print(roads1)
    #data = rawdata
    
    
    #print(roadsconnected)
    #tunnelsconnected = findConnectedRoads.connectLines(tunnels, "motorway", "F")
    roadsconnected = findConnectedRoads.connectLines(roads, "motorway", "F")
    bridgesconnected = findConnectedRoads.connectLines(bridges, "motorway", "T")

    roadsconnected2 = findConnectedRoads.connectLines(roads2, "primary", "F")
    bridgesconnected2 = findConnectedRoads.connectLines(bridges2, "primary", "T")
    roadsconnected1 = findConnectedRoads.connectLines(roads1, "secondary", "F")
    bridgesconnected1 = findConnectedRoads.connectLines(bridges1, "secondary", "T")

    roadsconnectedR = findConnectedRoads.connectLines(roadsR, "rail", "F")
    bridgesconnectedR = findConnectedRoads.connectLines(bridgesR, "rail", "T")

    #print(roadsR)
    #print(roadsconnectedR)

    data = {"type": "FeatureCollection", "features": []}
    data["features"] = roadsconnected + bridgesconnected + roadsconnected2 + bridgesconnected2 + roadsconnected1 + bridgesconnected1 + roadsconnectedR + bridgesconnectedR
    #data["features"] = roads["features"] + bridges["features"] + roads2["features"] + bridges2["features"] + roads1["features"] + bridges1["features"]
    ''''''
    #data["features"] + bridgesconnected
    #print(str(len(data["features"])) + "   ---  " + str(len(rawdata["features"])))
    segments = []
    selectedRoads = ["motorway","motorway_link","primary","secondary","trunk","trunk_link","unclassified", "tertiary", "service","residential","primary_link","secondary_link","rail"]
    thisroads = {}
    thisroads["features"] = []
    import random
    #print(data["features"][len(data["features"])-1])

    if len(data["features"]) > 0 :
        
        # first, cut segments at tile borders
        
        for sample in data["features"]:
            
            '''
            if sample["properties"]["highway"] in selectedRoads:
                 
                if sample["properties"]["highway"] == "motorway":
                    lanes = 3
                elif sample["properties"]["highway"] == "motorway_link":
                    lanes = 1
                else:
                    lanes = 2

                thisSegment = {}
                thisSegment["geometry"] = {}
                thisSegment["geometry"]["coordinates"] = []
                thisSegment["lanes"] = lanes
                thisSegment["bridge"] = 0
                thisSegment["tunnel"] = 0
                thisSegment["highway"] = sample["properties"]["highway"]


                    #print(int(sample["properties"]["lanes"]))
                if "bridge" in sample["properties"]:
                    thisSegment["bridge"] = 1
                if "tunnel" in sample["properties"]: # or "bridge" in sample["properties"]
                    thisSegment["tunnel"] = 1
                    thisSegment["bridge"] = 1
            '''
            if sample["properties"]["fclass"] in selectedRoads:

                if sample["properties"]["fclass"] == "rail":
                    lanes = 4
                    #print("ree")
                elif sample["properties"]["fclass"] == "motorway":
                    lanes = 3
                elif sample["properties"]["fclass"] == "primary":
                    lanes = 2
                else:
                    lanes = 1

                thisSegment = {}
                thisSegment["geometry"] = {}
                thisSegment["geometry"]["coordinates"] = []
                thisSegment["lanes"] = lanes
                thisSegment["bridge"] = 0
                thisSegment["tunnel"] = 0
                thisSegment["highway"] = sample["properties"]["fclass"]


                    #print(int(sample["properties"]["lanes"]))
                if  sample["properties"]["bridge"] == "T":
                    thisSegment["bridge"] = 1
                if  sample["properties"]["tunnel"]  == "T": # or "bridge" in sample["properties"]
                    thisSegment["tunnel"] = 1
                    #thisSegment["bridge"] = 1



                isInside = False
                p = sample["geometry"]["coordinates"][0]
                

                lastP = [0.00000001,0.000000000001]

                

                if p[0] < 1 and p[0] > 0 and p[1] < 1 and p[1] > 0 :
                    isInside = True
                #print("isinside " +str(isInside))
                count = 0
                for p in sample["geometry"]["coordinates"]:
                    count += 1
                    
                    if p[0] < 1 and p[0] > 0 and p[1] < 1 and p[1] > 0 :
                        
                        if not isInside:
                            #print("firstpoint inside")
                            isInside = True
                            ip = findIntersectionPoint(lastP,p)
                            x = [ip[0],ip[1],0] 
                            thisSegment["geometry"]["coordinates"].append(x)
                            #print(x)
                        thisSegment["geometry"]["coordinates"].append([p[0],p[1],0])
                        #print(p)

                    else:
                        if isInside:
                            ip = findIntersectionPoint(lastP,p)
                            x = [ip[0],ip[1],0] 
                            thisSegment["geometry"]["coordinates"].append(x)
                            segments.append(thisSegment)
                            thisSegment = {}
                            thisSegment["geometry"] = {}
                            thisSegment["geometry"]["coordinates"] = []
                            thisSegment["lanes"] = 0#sample["lanes"]
                            thisSegment["bridge"] = 0
                            thisSegment["tunnel"] = 0
                            
                            isInside = False
                            #print(sample)
                        #print("outside")
                    if count == len(p):
                        segments.append(thisSegment)
                    lastP = p

        #print(len(segments))
        count = 0   

        segmentsCopy = copy.deepcopy(segments)
        #print(segmentsCopy[10])     
        for s in segments:
            randomoffset = random.randint(-3, 3)
            stoffset = 0
            catoffset = (3 - s["lanes"])*5
            if count == 0 or count == len(segments)-1:
                stoffset = 10

            totalLength = 0
            bridgeheight = 0
            #print(s)
            s["properties"] = {}
            segmentsCopy[count]["properties"] = {}
            vl = len(verts)
            thisBridgeFeature = {}
            #thisBridgeFeature["geometry"] = {}

            
            thisBridgeFeature["coordinates"] = []
            #print(s)
            if not "lanes" in s:
                s["lanes"] = 1
            '''
            if "tunnel" in s:
                thisBridgeFeature["tunnel"] = s["tunnel"]
                #s["tunnel"]
            else:
                thisBridgeFeature["tunnel"] = 0
                s["tunnel"] = 0
            '''

            for i in range(len(s["geometry"]["coordinates"])):
                widthmulti = 1
                if s["lanes"] == 1:
                    widthmulti = 0.4
                elif s["lanes"] == 2:
                    widthmulti = 0.5
                elif s["lanes"] == 3:
                    widthmulti = 0.6
                elif s["lanes"] == 4:
                    widthmulti = 0.14
                #print(s["lanes"])

                

                if i > 0 :
                    AB = np.subtract(s["geometry"]["coordinates"][i-1], s["geometry"]["coordinates"][i])
                    BC = AB
                    if i < (len(s["geometry"]["coordinates"])-2):
                        BC = np.subtract(s["geometry"]["coordinates"][i], s["geometry"]["coordinates"][i+1])

                    length = np.linalg.norm(AB)
                    length1 = np.linalg.norm(BC)
                    


                    totalLength += length
                    
                    n1 = ([AB[1]*-1, AB[0],0]/length) * rwidth * widthmulti
                    n2 = n1 *-1
                    n12 = ([BC[1]*-1, BC[0],0]/length1) * rwidth * widthmulti
                    n22 = n12 *-1

                    na = (n1+n12)/2
                    nb = (n2+n22)/2

                    c = 0
                    if s["bridge"] == 1:
                        depth = 30
                    else:
                        depth = 80
                    
                    #print(i)
                    if i == 1:
                                        # get Z coordinate from hightmap
                        fcoords = [fix(s["geometry"]["coordinates"][i-1][0]), fix(s["geometry"]["coordinates"][i-1][1])]
                        #print(s["geometry"]["coordinates"][i-1])
                        c = hmap[int(fcoords[1]*32656)][int(fcoords[0]*32656)]
                        p0 = (s["geometry"]["coordinates"][i-1]+na) * size
                        p1 = (s["geometry"]["coordinates"][i-1]+nb ) * size
                        #print(str(int(s["geometry"]["coordinates"][i-1][1]*2041)) + "   "+ str(int(s["geometry"]["coordinates"][i-1][0]*2041)))
                        #print(c)
                        c = c * 1.5625 - 51200

                        verts.append([p0[0],p0[1],c- stoffset - catoffset + randomoffset]) #])
                        verts.append([p1[0],p1[1],c- stoffset - catoffset + randomoffset])#- stoffset - catoffset + randomoffset])
                        verts.append([p0[0],p0[1],c- depth ]+ na*size/100*depth) #])
                        verts.append([p1[0],p1[1],c- depth ]+ nb*size/100*depth) #])

                        UVs.append([0.75,0]) #1
                        UVs.append([0.25,0])
                        UVs.append([1,0]) 
                        UVs.append([0,0])

                        segmentsCopy[count]["geometry"]["coordinates"][0][2] =  c
                   # elif i == (len(s)-1):
                                                        # get Z coordinate from hightmap
                    #print(s)
                    if s["bridge"] == 1:
                        
                        bseg = len(s["geometry"]["coordinates"]) -1
                        c0 = hmap[int(s["geometry"]["coordinates"][0][1]*32656)][int(s["geometry"]["coordinates"][0][0]*32656)]*1.5625 - 51200
                        clast = hmap[int(s["geometry"]["coordinates"][bseg][1]*32656)][int(s["geometry"]["coordinates"][bseg][0]*32656)]*1.5625 - 51200
                        step = (clast - c0)/bseg
                        c = c0 + step*i

                        if i == 1:
                            thisBridgeFeature["coordinates"].append([s["geometry"]["coordinates"][0][0], s["geometry"]["coordinates"][0][1],c0])
                            thisBridgeFeature["lanes"] = s["lanes"]

                        thisBridgeFeature["coordinates"].append([s["geometry"]["coordinates"][i][0], s["geometry"]["coordinates"][i][1],c])
                         
                    else:
                        #print(str(int(s["geometry"]["coordinates"][i][1]*32656)) + "   "+ str(int(s["geometry"]["coordinates"][i][0]*32656)))
                        fcoords = [fix(s["geometry"]["coordinates"][i][0]), fix(s["geometry"]["coordinates"][i][1])]
                        fcoords1 = [fix(s["geometry"]["coordinates"][i-1][0]), fix(s["geometry"]["coordinates"][i-1][1])]
                        c = (hmap[int(fcoords[1]*32656)][int(fcoords[0]*32656)] )

                        c = c*1.5625 - 51200
                    
                #if i == (len(s["geometry"]["coordinates"])-1):
                    '''  
                    BC = np.subtract(s["geometry"]["coordinates"][i-1], s["geometry"]["coordinates"][i])

                    
                    length1 = np.linalg.norm(BC)
                    


                    totalLength += length1
                    
                 
                    n12 = ([BC[1]*-1, BC[0],0]/length1) * rwidth * widthmulti
                    n22 = n12 *-1

                    na = n12
                    nb = n22
                    #length = np.linalg.norm(np.subtract(s["geometry"]["coordinates"][i], s["geometry"]["coordinates"][i-1]))
                    ''' 
                    p0 = (s["geometry"]["coordinates"][i]+na)* size
                    p1 = (s["geometry"]["coordinates"][i]+nb)* size

                    
                    verts.append([p0[0],p0[1],c- stoffset - catoffset + randomoffset])# - stoffset - catoffset + randomoffset])
                    verts.append([p1[0],p1[1],c- stoffset - catoffset + randomoffset])# - stoffset - catoffset + randomoffset])
                    verts.append([p0[0],p0[1],c- depth ]+ na*size/100*depth)# ])
                    verts.append([p1[0],p1[1],c- depth ]+ nb*size/100*depth)# ])

                    UVs.append([0.75, totalLength * 1000]) #5
                    UVs.append([0.25, totalLength * 1000])
                    UVs.append([1, totalLength * 1000]) 
                    UVs.append([0, totalLength * 1000])
                    segmentsCopy[count]["geometry"]["coordinates"][i][2] =  c
                    
                if i < (len(s["geometry"]["coordinates"])-1):
                        '''
                        t1 = [2 + i*2 + vl, 1 + i*2 + vl, 3 + i*2 + vl]
                        t2 = [3 + i*2 + vl, 4 + i*2 + vl, 2 + i*2 + vl]
                        '''
                        t1 = [2 + i*4 + vl, 1 + i*4 + vl, 5 + i*4 + vl]
                        t2 = [5 + i*4 + vl, 6 + i*4 + vl, 2 + i*4 + vl]
                        t3 = [1 + i*4 + vl, 3 + i*4 + vl, 7 + i*4 + vl]
                        t4 = [7 + i*4 + vl, 5 + i*4 + vl, 1 + i*4 + vl]
                        t5 = [8 + i*4 + vl, 4 + i*4 + vl, 2 + i*4 + vl]
                        t6 = [2 + i*4 + vl, 6 + i*4 + vl, 8 + i*4 + vl]
                        t7 = [7 + i*4 + vl, 3 + i*4 + vl, 4 + i*4 + vl]
                        t8 = [4 + i*4 + vl, 8 + i*4 + vl, 7 + i*4 + vl]                        
                         
                        if s["lanes"] == 4:
                            trisRail.append(t1)
                            trisRail.append(t2)
                            trisRail.append(t3)
                            trisRail.append(t4)
                            trisRail.append(t5)
                            trisRail.append(t6)
                            trisRail.append(t7)
                            trisRail.append(t8)
                            #print("train")
                        elif s["lanes"] == 1:
                            
                            tris1Lane.append(t1)
                            tris1Lane.append(t2)
                            tris1Lane.append(t3)
                            tris1Lane.append(t4)
                            tris1Lane.append(t5)
                            tris1Lane.append(t6)
                            tris1Lane.append(t7)
                            tris1Lane.append(t8)

                        elif s["lanes"] == 2:
                            tris2Lane.append(t1)
                            tris2Lane.append(t2)
                            tris2Lane.append(t3)
                            tris2Lane.append(t4)
                            tris2Lane.append(t5)
                            tris2Lane.append(t6)
                            tris2Lane.append(t7)
                            tris2Lane.append(t8)
                            

                        elif s["lanes"] == 3:
                            tris3Lane.append(t1)
                            tris3Lane.append(t2)
                            tris3Lane.append(t3)
                            tris3Lane.append(t4)
                            tris3Lane.append(t5)
                            tris3Lane.append(t6)
                            tris3Lane.append(t7)
                            tris3Lane.append(t8)
                            
            # add caps 
            '''
            t1 = [1, 2, 3]
            t2 = [4, 3, 2]

            last = len(s["geometry"]["coordinates"]) - 4

            t3 = [last + 2, last + 1, last + 3]
            t4 = [last + 3, last + 4, last + 2]
            tris3Lane.append(t1)
            tris3Lane.append(t2)
            print("add cap")
            #tris1Lane.append(t3)
            #tris1Lane.append(t4)
            '''
                         
            if s["bridge"] == 1 or s["tunnel"] == 1:
                InstancedMeshBridges["features"].append(thisBridgeFeature)           
            count += 1
            #print(np.linalg.norm(AB)*1000)
        print("---------------")
        #print(segments)

        verts.append([0.0,0.0,0.0])
        verts.append([0.0,0.01,0.0])
        verts.append([0.01,0.0,0.0])

        UVs.append([0.0,0.0])
        UVs.append([0.0,0.01])
        UVs.append([0.01,0.0])

        tris1Lane.append([len(verts)-1,len(verts)-2,len(verts)-3])
        tris2Lane.append([len(verts)-1,len(verts)-2,len(verts)-3])
        tris3Lane.append([len(verts)-1,len(verts)-2,len(verts)-3])
        trisRail.append([len(verts)-1,len(verts)-2,len(verts)-3])


        for t in tunnels["features"]:
            l = len(t["coordinates"])-1
            fcoords = [fix(t["coordinates"][0][0]), fix(t["coordinates"][0][1])]
            fcoordsl = [fix(t["coordinates"][l][0]), fix(t["coordinates"][l][1])]
            fcoordsm = (np.array(fcoords) + np.array(fcoordsl))/2
            
            c = hmap[int(fcoords[1]*32656)][int(fcoords[0]*32656)] *1.5625 - 51200
            cl = hmap[int(fcoordsl[1]*32656)][int(fcoordsl[0]*32656)] *1.5625 - 51200

            if l < 3:
            #t["coordinates"][0].append(c)
                t["coordinates"] = [[t["coordinates"][0][0],t["coordinates"][0][1],int(c)], [fcoordsm[0], fcoordsm[1], int((c+cl)/2)], [fcoordsm[0], fcoordsm[1], int((c+cl)/2)], [t["coordinates"][l][0],t["coordinates"][l][1],int(cl)]]
            else:
                t["coordinates"] = [[t["coordinates"][0][0],t["coordinates"][0][1],int(c)], [t["coordinates"][1][0],t["coordinates"][1][1],int(c)], [t["coordinates"][l-1][0],t["coordinates"][l-1][1],int(cl)], [t["coordinates"][l][0],t["coordinates"][l][1],int(cl)]]
            
            InstancedMeshBridges["features"].append(t)
            #print(t) 

        out = {}
        out["features"] = segmentsCopy
        
         

        with open(name +"/Traffic_"+name+".json",mode="w") as f:
            json.dump(findConnectedRoads.findJunctions(out),f)
        #print(intersect([-1,   0.5],[1,   0.5],[0,    0],[0,    1]))
          
        #print(InstancedMeshBridges)
        with open(name +"/Bridges_"+name+".json",mode="w") as f:
            json.dump(InstancedMeshBridges,f)

        open(name +'/roads_'+name+'.obj', 'w').close()
        with open(name +'/roads_'+name+'.obj', 'w') as f1:
            for v in verts:
                line = "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + '\n'
                f1.write(line)

            for u in UVs:
                line = "vt " + str(u[0]) + " " + str(u[1]) +'\n'
                f1.write(line)

 
            f1.write('\ng 1Lane\nusemtl 1Lane\n')
            
            for t in tris1Lane:
                line = "f " + str(t[0]) + "/" + str(t[0]) + " "+ str(t[1]) + "/" +str(t[1]) +" "+ str(t[2]) + "/"+ str(t[2]) + '\n'
                f1.write(line)

            f1.write('\ng 2Lane\nusemtl 2Lane\n')
            for t in tris2Lane:
                line = "f " + str(t[0]) + "/" + str(t[0]) + " "+ str(t[1]) + "/" +str(t[1]) +" "+ str(t[2]) + "/"+ str(t[2]) + '\n'
                f1.write(line)

            f1.write('\ng 3Lane\nusemtl 3Lane\n')
            for t in tris3Lane:
                line = "f " + str(t[0]) + "/" + str(t[0]) + " "+ str(t[1]) + "/" +str(t[1]) +" "+ str(t[2]) + "/"+ str(t[2]) + '\n'
                f1.write(line)

            f1.write('\ng rail\nusemtl rail\n')
            for t in trisRail:
                line = "f " + str(t[0]) + "/" + str(t[0]) + " "+ str(t[1]) + "/" +str(t[1]) +" "+ str(t[2]) + "/"+ str(t[2]) + '\n'
                f1.write(line)
            
            

    else:
        print("empty")

























def cropGeoJsonLineFeature(name):
    # Rivers
    hmap = cv2.imread(name +'/hmap_burnIn_noRiver'+ name +'.png', cv2.IMREAD_UNCHANGED)
    size = 204200
    f = open(name+'/power_'+name+'.json')
    data = json.load(f)

    segments = {}
    segments["features"] = []

    if len(data["features"])>0 :

        # first, cut segments at tile borders
        for sample in data["features"]:
            isInside = False
            p = sample["geometry"]["coordinates"][0]
            thisfeature = {}
            thisfeature["coordinates"] = []
            lastP = [0,0]

            

            if p[0] < 1 and p[0] > 0 and p[1] < 1 and p[1] > 0 :
                isInside = True

            count = 0
            for p in sample["geometry"]["coordinates"]:
                count += 1
                if p[0] < 1 and p[0] > 0 and p[1] < 1 and p[1] > 0 :
                    
                    if not isInside:
                        #print("firstpoint inside")
                        isInside = True
                        ip = findIntersectionPoint(lastP,p)
                        c = hmap[int(ip[1]*2040.9)][int(ip[0]*2040.9)]*1.5625 - 51200
                        x = [ip[0]*size,ip[1]*size,c] 
                        #thisSegment.append(x)
                        thisfeature["coordinates"].append(x)
                        #print(x)

                    c = hmap[int(p[1]*2040.9)][int(p[0]*2040.9)]*1.5625 - 51200
                    x = [p[0]*size,p[1]*size,c]
                   # thisSegment.append(x)
                    thisfeature["coordinates"].append(x)
                    #print(p)

                else:
                    if isInside:
                        ip = findIntersectionPoint(lastP,p)
                        c = hmap[int(ip[1]*2040.9)][int(ip[0]*2040.9)]*1.5625 - 51200
                        x = [ip[0]*size,ip[1]*size,c]
                        #thisSegment.append(x)

                        thisfeature["coordinates"].append(x)

                        #segments.append(thisSegment)
                        segments["features"].append(thisfeature)
                        thisfeature["coordinates"] = []
                        #thisSegment = []
                        isInside = False
                        #print(p)
                    #print("outside")
                if count == len(p):
                    #segments.append(thisSegment)
                    segments["features"].append(thisfeature)
                lastP = p

        #print(segments)

       

        for f in range (len(segments["features"])):
            for i in range (len(segments["features"][f]["coordinates"])):
                if i == 0:
                    p = [segments["features"][f]["coordinates"][i][0],segments["features"][f]["coordinates"][i][1]]
                    p1 = [segments["features"][f]["coordinates"][i+1][0],segments["features"][f]["coordinates"][i+1][1]]
                    v = np.subtract(p, p1)
                    angle2 = np.arctan2(v[1], v[0]) - np.arctan2(0,1)

                    print(np.rad2deg(angle2))
                    segments["features"][f]["coordinates"][i].append(np.rad2deg(angle2))
                else:
                    p1 = [segments["features"][f]["coordinates"][i][0],segments["features"][f]["coordinates"][i][1]]
                    p = [segments["features"][f]["coordinates"][i-1][0],segments["features"][f]["coordinates"][i-1][1]]
                    v = np.subtract(p, p1)
                    angle2 = np.arctan2(v[1], v[0]) - np.arctan2(0,1)

                    print(np.rad2deg(angle2))
                    segments["features"][f]["coordinates"][i].append(np.rad2deg(angle2))
        json_object = json.dumps(segments)
    # Writing to sample.json
        with open(name+"/PowerReady_"+ name+".json", "w") as outfile:
            outfile.write(json_object)

    else:
        print("empty")



def copyfiles(src_path, destination_path):

    if os.path.isfile(src_path):
        cp(src_path, destination_path)
    else:
        print("couldnt find "+ src_path)

#cropGeoJsonLineFeature(name)
'''
n = "0_-1"
makeRoadMesh((0,-1))
#makeRiverMesh(n)

src_path = n +'/'+"roads_"+n+'.obj'
destination_path = 'worldmachine_json/newroads/rw_X30_Y16.obj'
copyfiles(src_path,destination_path)
#overpassQuery.cropGeoJsonPoly((0,-1),'austriaShapefiles/austria_roads-selected.geojson','roadssmooth')
#overpassQuery.cropGeoJsonPoly((0,-1),'austriaShapefiles/austria_roads-selected.geojson','roadssmooth')     
#

'''