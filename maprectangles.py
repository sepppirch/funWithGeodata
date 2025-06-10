import json
import os
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
                sorted.append([number,number1])
            except ValueError:
                print("some_variable did not contain a number!")
        except ValueError:
            print("some_variable did not contain a number!")
        #print(vals)
        
print(sorted)

                  

def makegrid():
#for i,u in sorted:
    geoj = json.loads("""
    {
    "type": "FeatureCollection",
    "name": "test",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": [

        ]
    }
    """)
    for i in range(-16,24):
        for u in range (-16,54):
            argh = json.loads("""
                {
                    "type": "Feature",
                    "name":"",
                    "geometry":
                    {
                    
                    "type": "Polygon",
                    "coordinates": [

                    ]
                }
                
                }""")
            center = (47.48802456352513, 13.233287974359211)
            h=0.1096
            w=0.16
            bigtile = [16-i,u-31]
            topLeft = [center[1] + bigtile[1] * w, center[0] - bigtile[0] * h]
            bottomRight = [topLeft[0]+ w, topLeft[1]- h]
            tr = [topLeft[0],bottomRight[1]]
            bl = [bottomRight[0], topLeft[1]]

            name = str(bigtile[0])+"_"+str(bigtile[1])
            newname = " | X" + str(u) +"_Y" + str(i)
            name = name + newname
            #print(topLeft)
            coords = [topLeft,tr,bottomRight,bl]

            argh["geometry"]["coordinates"] = [coords]
            argh["name"]= name

            geoj["features"].append(argh)
    return geoj    






def drawSectors():
    sectors = [[-19,-31],[-19,-13],[-19,5],[-1,-49],[-1,-31],[-1,-13],[-1,5],[17,-49]]
    names = ["A","B","C","D","E","F","G","H"]
    geoj = json.loads("""
    {
    "type": "FeatureCollection",
    "name": "test",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": [

        ]
    }
    """)
    c = 0
    for u in sectors:
        argh = json.loads("""
            {
                "type": "Feature",
                "name":"",
                "geometry":
                {
                
                "type": "Polygon",
                "coordinates": [

                ]
            }
            
            }""")
        center = (47.48802456352513, 13.233287974359211)
        h=0.1096
        w=0.16
        bigtile = [u[0],u[1]]
        topLeft = [center[1] + bigtile[1] * w, center[0] - bigtile[0] * h]
        bottomRight = [topLeft[0]+ w*18, topLeft[1]- h*18]
        tr = [topLeft[0],bottomRight[1]]
        bl = [bottomRight[0], topLeft[1]]

        name = str(bigtile[0])+"_"+str(bigtile[1])
        newname = " | X" + str(u[1]+31) +"_Y" + str(16 - u[0])
        newname = names[c] 
        #print(topLeft)
        coords = [topLeft,tr,bottomRight,bl]
        print(name)
        if os.path.isfile( name + "/landscape.stl"):
            print("has stl")
            argh["stl"] = 1
        else:
            argh["stl"] = 0
        argh["geometry"]["coordinates"] = [coords]
        argh["name"]= newname

        geoj["features"].append(argh)
        c =c+1

    return geoj
 











def vizFiles(files):
    geoj = json.loads("""
    {
    "type": "FeatureCollection",
    "name": "test",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": [

        ]
    }
    """)
    for u in files:
        argh = json.loads("""
            {
                "type": "Feature",
                "name":"",
                "geometry":
                {
                
                "type": "Polygon",
                "coordinates": [

                ]
            }
            
            }""")
        center = (47.48802456352513, 13.233287974359211)
        h=0.1096
        w=0.16
        bigtile = [u[0],u[1]]
        topLeft = [center[1] + bigtile[1] * w, center[0] - bigtile[0] * h]
        bottomRight = [topLeft[0]+ w, topLeft[1]- h]
        tr = [topLeft[0],bottomRight[1]]
        bl = [bottomRight[0], topLeft[1]]

        name = str(bigtile[0])+"_"+str(bigtile[1])
        newname = " | X" + str(u[1]+31) +"_Y" + str(16 - u[0])
        newname = name + newname
        #print(topLeft)
        coords = [topLeft,tr,bottomRight,bl]
        print(name)
        if os.path.isfile( name + "/landscape.stl"):
            #print("has stl")
            argh["stl"] = 1
        else:
            argh["stl"] = 0
        argh["geometry"]["coordinates"] = [coords]
        argh["name"]= newname

        geoj["features"].append(argh)
    return geoj 



data = vizFiles(sorted)
#data = drawSectors()
json_object = json.dumps(data, indent=4)
 
# Writing to sample.json
with open("test.geojson", "w") as outfile:
    outfile.write(json_object)