import csv 
import os
import json
files = os.listdir("_Waypoints")
print(files)

geoj = json.loads("""
{
"type": "FeatureCollection",
"name": "test",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
    "features": [
    ]
}
""")

for f in files:
# Open file  
    with open('_Waypoints/'+f) as file_obj: 
        
        # Create reader object by passing the file  
        # object to reader method 
        reader_obj = csv.reader(file_obj) 
        
        # Iterate over each row in the csv  
        # file using reader object 
        for row in reader_obj:

            argh = json.loads("""
            {
                "type": "Feature",
                "name":"",
                "conf":100,
                "geometry":
                {
                
                "type": "Point",
                "coordinates": [

                ]
            }
            
            }""")
            #
            try:
                argh["geometry"]["coordinates"] = [float(row[1]), float(row[0])]
                argh["conf"]=int(row[3])
                geoj["features"].append(argh)
                #print(float(str(row[3]).replace("N",""))/100)
            except:
                print("err")

#print(geoj)
json_object = json.dumps(geoj, indent=4)
 
# Writing to sample.json
with open("_Waypoints/thermals.geojson", "w") as outfile:
    outfile.write(json_object)