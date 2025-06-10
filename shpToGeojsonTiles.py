import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import pandas as pd
import cv2
import math
import numpy as np
import findConnectedRoads
import json
import postprocessHmap

# dont change
center = (47.48802456352513, 13.233287974359211)

h=0.1096
w=0.16

for x in range (9):
    for y in  range(6):
        bigtile = (y-1,x-4)
        print(bigtile)
        postprocessHmap.closegaps(bigtile[0],bigtile[1])
        
        name = str(bigtile[0])+"_"+str(bigtile[1])

        topleft = (center[1] + bigtile[1] * w, center[0] - bigtile[0] * h)
        bbox=(topleft[0],topleft[1],topleft[0]+w,topleft[1]-h)
        '''
        roads = gpd.read_file('austriaShapefiles/gis_osm_roads_free_1.shp',bbox=bbox)
        roads.crs = "EPSG:4326"
        roads.to_crs(epsg=4258)
        #roads.clip_by_rect(topleft[1]-h,topleft[0],topleft[1],topleft[0]+w)
        roads.to_file("roadsClipped"+ name+".json", driver="GeoJSON")
        '''
        lakes = gpd.read_file('alpsGeoJSON/alps_lakes_sp.geojson', bbox=bbox)
        
        lakes.to_file(name+"/lakes"+ name+".json", driver="GeoJSON")

        rivers = gpd.read_file('alpsGeoJSON/alps_rivers_sp.geojson', bbox=bbox)
        rivers.to_file(name+"/rivers"+ name+".json", driver="GeoJSON")

        highways = gpd.read_file('alpsGeoJSON/alps_highways.geojson', bbox=bbox)
        highways.to_file(name+"/highways"+ name+".json", driver="GeoJSON")

        path = name+"/highways"+ name+".json"
        with open(path, 'r') as f:
            data = json.load(f)
            highways = findConnectedRoads.findJunctions(data)

            json_object = json.dumps(data)
    
    # Writing to sample.json
            with open(name+"/highways"+ name+".json", "w") as outfile:
                outfile.write(json_object)