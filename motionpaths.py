import json
import random
import findConnectedRoads
import cv2


def fix(input):
    if input < 0:
        return 0.00000001
    elif input > 0.99999999:
        return 0.9999999
    else:
        return input





name = "1_-1"
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

points={"coordinates":[]}
for i in range(100):
    if len(trains["features"][start]["properties"]["nextSegments"]) > 0:
        totlen = totlen+ float(trains["features"][start]["properties"]["length_3"])
        first = True
        for p in trains["features"][start]["geometry"]["coordinates"]:
            fcoords = [fix(p[1])*32656, fix(p[0])*32656]
            c = float(hmap[int(fcoords[0])][int(fcoords[1])]*1.5625 - 51200)
            thisp = [p[0],p[1],c]
            if not first:
                points["coordinates"].append(thisp)
            first = False
        start = trains["features"][start]["properties"]["nextSegments"][0]
        
    else:
        print("finished " + str(totlen))
        print(points)
        with open(name +"/trains_"+name+".json",mode="w") as f:
            json.dump(points,f)
        break
#print(trains[start]["properties"])

#with open(name +"/Traffic_"+name+".json",mode="w") as f:
