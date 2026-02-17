import overpass
import geopandas as gpd
import geojson
import json
# up / left 

#bigtile = (-1,-2)
h=0.1096
w=0.16

def downloadGeoJson(bigtile, query, Gtype , outfilename):
    data = {}
    data["features"] = []
    try:
        center = (47.48802456352513 + h * bigtile[0] * -1, 13.233287974359211 + w * bigtile[1])
        api = overpass.API(timeout=500)
        name = str(bigtile[0])+"_"+str(bigtile[1])
        #result = api.get("""way["building"](40.0627513928,-2.1478584892,40.0845316612,-2.1151342638);""",verbosity='geom')

        #result = api.get("""way["highway"];relation["highway"](40.0627513928,-2.1478584892,40.0845316612,-2.1151342638);""",verbosity='geom')
        #query = 'way["landuse"]'
        result = api.get(query +"""("""+ str(center[0]-h)+""", """+str(center[1])+""", """ + str(center[0]) +""", """+ str(center[1]+w)+""");(._;>;)""", responseformat = "geojson", verbosity='geom')  
        #result = api.get( query +"""("""+ str(center[0]-h)+""", """+str(center[1])+""", """ + str(center[0]) +""", """+ str(center[1]+w)+""");(._;>;)""", responseformat = "geojson", verbosity='geom')
        #print(result)


        
        for i in result["features"]:
            #print(i)
            if i["geometry"]["type"] == Gtype:
                data["features"].append(i)
            

                normalized = []
                if i["geometry"]["type"] == "LineString" :
                    for p in i["geometry"]["coordinates"]:
                        norm = [(p[0] - center[1]) * 1 / w, (p[1] - center[0]) * 1 / h * -1]
                        normalized.append(norm) 
                        #print(norm)
                if i["geometry"]["type"] == "Point" :
                        p = i["geometry"]["coordinates"]
                        norm = [(p[0] - center[1]) * 1 / w, (p[1] - center[0]) * 1 / h * -1]
                        normalized.append(norm)

                        
                i["geometry"]["coordinates"] = normalized


    except:
         print("error downloading geojson")
        #geojson.dump(result,f)            
    with open(name +"/"+ outfilename +"_"+name+".json",mode="w") as f:
        geojson.dump(data,f)






def cropGeoJsonPoly(bigtile, infilename, outfilename):
        
        name = str(bigtile[0])+"_"+str(bigtile[1])
        center = (47.48802456352513 + h * bigtile[0] * -1, 13.233287974359211 + w * bigtile[1])
        bbox=(center[1],center[0],center[1]+ w, center[0] - h)

        data = gpd.read_file(infilename, bbox=bbox)
        data = json.loads(data.to_json())
        for i in data["features"]:
            normalized = []
            if i["geometry"]["type"] == "Polygon":
                for p in i["geometry"]["coordinates"][0]:
                    norm = [(p[0] - center[1]) * 1 / w, (p[1] - center[0]) * 1 / h * -1]
                    normalized.append(norm)

            if i["geometry"]["type"] == "LineString" :
                for p in i["geometry"]["coordinates"]:
                    norm = [(p[0] - center[1]) * 1 / w, (p[1] - center[0]) * 1 / h * -1]
                    normalized.append(norm)

            if i["geometry"]["type"] == "Point" :
                p = i["geometry"]["coordinates"]
                norm = [(p[0] - center[1]) * 1 / w, (p[1] - center[0]) * 1 / h * -1]
                normalized.append(norm)
                #norm = [(p[0] - center[1]) * 1 / w, (p[1] - center[0]) * 1 / h * -1]
                #normalized.append(norm)

            i["geometry"]["coordinates"] = normalized

        with open(name +"/"+ outfilename +"_"+name+".json",mode="w") as f:
            geojson.dump(data,f)
        #data1.to_file(name + "/" + outfilename + "_"  + name+".json", driver="GeoJSON")
#downloadGeoJson((0,0),'relation["type"="multipolygon"]',"LineString", 'forestX')



#downloadGeoJson((4,-1),'way[man_made=snow_fence]',"LineString", 'test')
#downloadGeoJson((6,-29),'way[power=line]',"LineString", 'power')
#downloadGeoJson((5,-8),'node[natural=peak]',"Point", 'peaks')
#downloadGeoJson((6,-29),'node[natural=peak]',"Point", 'peaks')
#downloadGeoJson((5,-29),'node[place=village]',"Point", 'village')
#downloadGeoJson((6,-29),'node[sport=free_flying]',"Point", 'freefly')


