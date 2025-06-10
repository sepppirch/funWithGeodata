import json
import os
import shutil 
from shutil import copy
import os.path

dirs = os.listdir()
sorted = []
for x in dirs:
    if "_" in x:
        vals = x.split("_")
        try:
            number = int(vals[0])
            try:
                number1 = int(vals[1])
                sorted.append(x)
            except ValueError:
                print("some_variable did not contain a number!")
        except ValueError:
            print("some_variable did not contain a number!")
print(sorted)

def copyfiles(name, newname, wpath):
    #folders = ["forest","grass","hmaps","rocks"]
    #prefix = ["f_","g_","h_","r_"]
    folders = ["hmaps"]
    prefix = ["h_"]

    for i in range (len(folders)):
         
        src_path = name +'/'+folders[i]+'n'+name+'.png'
        if folders[i]=="hmaps":
            src_path = name +'/'+'hmap_burnIn_'+name+'.png'
        print(src_path)
        destination_path = wpath+'/'+ folders[i]+'/'+prefix[i]+newname+'.png'
        
        copy(src_path, destination_path)

geoj = json.loads("""
    {
    "type": "FeatureCollection",
    "name": "test",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": [

        ]
    }
    """)



names = []
foundnames =[]
sectors = [[-2,-31],[-2,-13],[-2,5],[16,-49],[16,-31],[16,-13],[16,5],[34,-49]]
snames = ["A","B","C","D","E","F","G","H"]
wpath = "worldmachine_G"
folders = ["forest","grass","hmaps","rocks"]
prefix = ["f_","g_","h_","r_"]

with open('tileselection.geojson', 'r') as file:
    data = json.load(file)
    for f in data["features"]:
        n = f["properties"]["name"].split("|")
        names.append(str(n[0]).replace(" ",""))

#print(names)
bottomLeft = sectors[6]
#bottomLeft = [topleft[0]+17,topleft[1]]
#bottomLeft = [16  ,-31]

for x in range (18):
    for y in  range(18): 
        bigtile = (bottomLeft[1] + y, bottomLeft[0] - x )
        name = str(bigtile[1])+"_"+str(bigtile[0])
        newname = "_X"+ str(y) +"_Y" + str(x)
        #print(name)
        if name in sorted:
            if name in names: 
                copyfiles(name,newname,wpath)
                foundnames.append(name)
                print(str(name) + " in tileset") 

with open('tileselection.geojson', 'r') as file:
    data = json.load(file)
    for f in data["features"]:
        n = f["properties"]["name"].split("|")
        n = str(n[0]).replace(" ","")
        #print(n)
        if n in foundnames:
            
            geoj["features"].append(f)  
        #
json_object = json.dumps(geoj, indent=4)
 
# Writing to sample.json
with open("G.geojson", "w") as outfile:
    outfile.write(json_object)