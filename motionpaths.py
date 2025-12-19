import json
import random

name = "1_-1"
f = open(name+'/Traffic_'+name+'.json')
rawdata = json.load(f)

trains = []

for s in rawdata["features"]:
    if "highway" in s:
        if s["highway"] == "rail":
            trains.append(s)
            

start = random.randrange(0, len(trains)-1)

print(trains[start]["properties"]["length_3"])