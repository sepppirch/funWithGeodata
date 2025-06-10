import geopandas as gpd
import json
import copy
import numpy as np
'''
gj = gpd.read_file('buildings_werfenJSON.geojson', driver='GeoJSON')
print(gj.head())


for row in gj:
    print(row["geometry"])
'''


def findJunctions(data):

    
    count = 0

    # calculate section lengths:

    for z in data["features"]:
        z["properties"]["lastSegments"] = []
        z["properties"]["nextSegments"] = []

        newLength = 0
        for i in range(len(z["geometry"]["coordinates"]) - 1):
            thisP = np.array(z["geometry"]["coordinates"][i])
            nextP = np.array(z["geometry"]["coordinates"][i +1])
            l = np.linalg.norm(thisP - nextP)

            newLength += l
            #print(l) 

        z["properties"]["length_3"] = newLength * 100000
        z["properties"]["id"] = count
        count += 1


    count1 = 0

    for i in data["features"]:
        if len(i["geometry"]["coordinates"])>0:
            last = i["geometry"]["coordinates"][int(len(i["geometry"]["coordinates"])-1)]
            #print(last)
            count = 0
        
    
        for x in data["features"]:
            ##print(x)
            if len(x["geometry"]["coordinates"])>0:
                othersFirst = x["geometry"]["coordinates"][0]
                difnext = (last[0] - othersFirst[0]) + (last[1] - othersFirst[1])

                if difnext  == 0:
                    #print("next found" + str(count))
                    i["properties"]["nextSegments"].append(count)  
                    x["properties"]["lastSegments"].append(count1)
            
            count += 1
        count1 += 1

    return data




def combineMultiSegment(data):
    bridgedata = {}
    bridgedata["features"] = []

    outdata = {}
    outdata["features"] = []

    for f in data["features"]:
        if "bridge" in f["properties"]:
            bridgedata["features"].append(f)
        else:
            outdata["features"].append(f)



    x = findJunctions(bridgedata) #print(x)
    counter = 0

    multisegbridges = []
    for sample in x["features"]:
        if "bridge" in sample["properties"]:

            if len(sample["properties"]["lastSegments"]) == 0 and len(sample["properties"]["nextSegments"]) == 0:
                outdata["features"].append(sample)
            if len(sample["properties"]["nextSegments"]) > 0:
                if len(sample["properties"]["lastSegments"]) == 0:
                    #print("beginning found")
                    search = True
                    
                    nextf = sample["properties"]["nextSegments"][0]
                    thisbridge = []
                    thisbridge.append(counter)
                    thisbridge.append(nextf)

                    while search == True:
                    #print(x["features"][nextf]["properties"]["nextSegments"])
                        
                        if len(x["features"][nextf]["properties"]["nextSegments"]) > 0:
                            if x["features"][nextf]["properties"]["nextSegments"][0] not in thisbridge:
                                #print("next segment")
                            
                                #print (nextf)
                                nextf = x["features"][nextf]["properties"]["nextSegments"][0]

                                thisbridge.append(nextf)
                            else:
                                search = False
                        else:
                            search = False
                    multisegbridges.append(thisbridge)
                    #print(thisbridge)
                    
            #if isFirst == True and isLast == False:
            #print(str(counter) + " next " + str(sample["properties"]["nextSegments"]) + " prev " + str(sample["properties"]["lastSegments"]))
                
        counter += 1

    combinedFeatures = []
    #print(multisegbridges)


    for bridge in multisegbridges:
    
        newfeature = copy.deepcopy(x["features"][bridge[0]])
        count = 0
        for f in bridge:
            if count > 0:
                count2 = 0
                for p in x["features"][f]["geometry"]["coordinates"]:
                    
                    if count2 > 0:
                        newfeature["geometry"]["coordinates"].append(p)
                    count2 += 1
            count += 1
        #print(newfeature)
        
        combinedFeatures.append(newfeature)

    for c in combinedFeatures:
        outdata["features"].append(c)

    return outdata








def combineMultiSegmentLines(data):

    outdata = {}
    outdata["features"] = []

    x = findJunctions(data) #print(x)
    counter = 0

    multisegbridges = []
    for sample in x["features"]:
        
        if len(sample["properties"]["lastSegments"]) == 0 and len(sample["properties"]["nextSegments"]) == 0:
            outdata["features"].append(sample)
        if len(sample["properties"]["nextSegments"]) > 0:
            if len(sample["properties"]["lastSegments"]) == 0:
                print("beginning found")
                search = True
                
                nextf = sample["properties"]["nextSegments"][0]
                thisbridge = []
                thisbridge.append(counter)
                thisbridge.append(nextf)

                while search == True:
                #print(x["features"][nextf]["properties"]["nextSegments"])
                    
                    if len(x["features"][nextf]["properties"]["nextSegments"]) > 0:
                        if x["features"][nextf]["properties"]["nextSegments"][0] not in thisbridge:
                            print("next segment")
                        
                            print (nextf)
                            nextf = x["features"][nextf]["properties"]["nextSegments"][0]

                            thisbridge.append(nextf)
                        else:
                            search = False
                    else:
                        search = False
                multisegbridges.append(thisbridge)
                #print(thisbridge)
                
        #if isFirst == True and isLast == False:
        #print(str(counter) + " next " + str(sample["properties"]["nextSegments"]) + " prev " + str(sample["properties"]["lastSegments"]))
            
        counter += 1

    combinedFeatures = []
    #print(multisegbridges)


    for bridge in multisegbridges:
    
        newfeature = copy.deepcopy(x["features"][bridge[0]])
        count = 0
        for f in bridge:
            if count > 0:
                count2 = 0
                for p in x["features"][f]["geometry"]["coordinates"]:
                    
                    if count2 > 0:
                        newfeature["geometry"]["coordinates"].append(p)
                    count2 += 1
            count += 1
        #print(newfeature)
        
        combinedFeatures.append(newfeature)

    for c in combinedFeatures:
        outdata["features"].append(c)

    return outdata
'''
name = "0_0"
f = open(name+'/roads_'+name+'.json')
data = json.load(f)

print(combineMultiSegment(data))

name = "8_-31"
f = open(name+'/rivers_'+name+'.json')
data = json.load(f)
print(len(combineMultiSegmentLines(data)))
'''