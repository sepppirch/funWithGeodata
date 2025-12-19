import geopandas as gpd
import json
import copy
import numpy as np
import cv2
import shapely
from shapely import MultiLineString

size = 204000
verts = []
UVs = []
tris3 = []
tris2 = []
tris1 = []

samplesHighway = {"type": "FeatureCollection","features":[]}
samplesHighwayBridge = {"type": "FeatureCollection","features":[]}
samplesPrimary = {"type": "FeatureCollection","features":[]}
samplesPrimaryBridge = {"type": "FeatureCollection","features":[]}
samplesSecondary = {"type": "FeatureCollection","features":[]}
samplesSecondaryBridge = {"type": "FeatureCollection","features":[]}

def connectLines(data):
    shpData = shapely.from_geojson(json.dumps(data))
    merged = shapely.line_merge(shpData)
    mergedList = [list(x.coords) for x in merged.geoms]
    outlist = []
    for sample in mergedList:
        thissample = []
        for p in sample:
            if p[0] < 1 and p[0] > 0 and p[1] < 1 and p[1] > 0 :
                thissample.append([float(p[0]),float(p[1])])
                
        outlist.append(thissample)



    return outlist

def addMeshData(data, hmap, target, w, h, bridge):
    vl = len(verts)
    for s in data:
        
        totalLength = 0
        for i in range(len(s)):
            #
            if bridge == False:
                
                if i > 0:
                    #print(s[i])
                    AB = np.subtract(s[i-1], s[i])
                    length = np.linalg.norm(AB)
                    totalLength += length
                    n1 = ([AB[1]*-1, AB[0],0]/length) * w 
                    n2 = n1 *-1
                    n12 = n1
                    n22 = n2


                    na3 = (n1+n12)/2
                    na = [na3[0],na3[1]]
                    #print(na)
                    nb3 = (n2+n22)/2
                    nb = [nb3[0],nb3[1]]
                    c = 0

                    if i == 1:
                        
                            #print(size)
                            c = hmap[int(s[i-1][1]*2040)][int(s[i-1][0]*2040)]*1.5625 - 51200
                            p0 = np.multiply(np.add(s[i-1] , na),size)
                            p1 = np.multiply(np.add(s[i-1], nb),size) 
                            
                            
                            verts.append([p0[0],p0[1],c])
                            verts.append([p1[0],p1[1],c])
                            verts.append([p0[0],p0[1],c - h])
                            verts.append([p1[0],p1[1],c - h])
                            
                            UVs.append([0.75,0]) #1
                            UVs.append([0.25,0])
                            UVs.append([1,0]) 
                            UVs.append([0,0])
                        
                            #("hmaplookup failed - ignoring")
                            #break

                    else:
                        
                            c = hmap[int(s[i][1]*2040)][int(s[i][0]*2040)]*1.5625 - 51200

                        
                            ("hmaplookup failed - ignoring")
                            #break

                    length = np.linalg.norm(np.subtract(s[i], s[i-1]))
                    '''
                    pp0 = (s[i]+list(na))
                    p0 = pp0 * size
                    pp1 = (s[i]+list(nb))
                    p1 = pp1 * size
                    '''
                    p0 = np.multiply(np.add(s[i],na),size)
                    p1 = np.multiply(np.add(s[i],nb),size) 
                    #print(p0)
                    verts.append([p0[0],p0[1],c])
                    verts.append([p1[0],p1[1],c])
                    verts.append([p0[0],p0[1],c - h]+list(na)*size)
                    verts.append([p1[0],p1[1],c - h]+list(nb)*size)
                    
                    UVs.append([0.75, totalLength * 1000]) #5
                    UVs.append([0.25, totalLength * 1000])
                    UVs.append([1, totalLength * 1000]) 
                    UVs.append([0, totalLength * 1000])

                    if i < len(s)-1:
                        t1 = [2 + i*4 + vl, 1 + i*4 + vl, 5 + i*4 + vl]
                        t2 = [5 + i*4 + vl, 6 + i*4 + vl, 2 + i*4 + vl]
                        t3 = [1 + i*4 + vl, 3 + i*4 + vl, 7 + i*4 + vl]
                        t4 = [7 + i*4 + vl, 5 + i*4 + vl, 1 + i*4 + vl]
                        t5 = [8 + i*4 + vl, 4 + i*4 + vl, 2 + i*4 + vl]
                        t6 = [2 + i*4 + vl, 6 + i*4 + vl, 8 + i*4 + vl]
                        t7 = [7 + i*4 + vl, 3 + i*4 + vl, 4 + i*4 + vl]
                        t8 = [4 + i*4 + vl, 8 + i*4 + vl, 7 + i*4 + vl]
                        target.append(t1)
                        target.append(t2)
                        target.append(t3)
                        target.append(t4)
                        target.append(t5)
                        target.append(t6)
                        target.append(t7)
                        target.append(t8)

                    

def makeRoadMesh(bigtile):
    name = str(bigtile[0])+"_"+str(bigtile[1])
    hmap = cv2.imread(name +'/hmap_burnIn_noRiver'+name+'.png', cv2.IMREAD_UNCHANGED)
    f = open(name+'/roadssmooth_'+name+'.json')
    data = json.load(f)

    #sort by road type
    for sample in data["features"]:
        if sample["properties"]["fclass"] == "primary":
            if sample["properties"]["bridge"] == "T":
                samplesHighwayBridge["features"].append(sample)
            else:
                samplesHighway["features"].append(sample)
        
    # connect segments
    
    sorted = connectLines(samplesHighway)
    #print(sorted[0])
    addMeshData(sorted, hmap, tris1, 0.0022, 40, False)
    #print (verts)
    with open(name +'/roads_'+name+'.obj', 'w') as f1:
        for v in verts:
            line = "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + '\n'
            f1.write(line)

        for u in UVs:
            line = "vt " + str(u[0]) + " " + str(u[1]) +'\n'
            f1.write(line)

 
        f1.write('\ng 1Lane\nusemtl 1Lane\n')
        '''
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
        '''
        
        for t in tris1:
            line = "f " + str(t[0]) + "/" + str(t[0]) + " "+ str(t[1]) + "/" +str(t[1]) +" "+ str(t[2]) + "/"+ str(t[2]) + '\n'
            f1.write(line)

makeRoadMesh((1,-1))