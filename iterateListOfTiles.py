import json
import os
import shutil 
from shutil import copy
import os.path
import makeLakes
import postprocessHmap
#import makeBuildingGeometry
import makeLandscapeMesh
import normalfromhightmap
import cv2
#import overpassQuery
import landuse
import masks
#import segmentSatImage
import numpy as np
import thermalcalculator
import overpassQuery
names = []
newnames = []
jsonfiles = [""]
wpath = "worldmachine_json/thermalsGen"
### iterate all tiles in tileselection 
#
def copyfiles(src_path, destination_path):
    #folders = ["aerialways","bridges","PowerReady","lakes","peaks","talwind"]
    #prefix = ["aerialway_","bridge_","cables_","lakes_","peaks_","talwind_"]
    #folders = ["rivers","roads, building"]
    #prefix = ["river_","rw_","b_"]


    #src_path = name +'/'+folder+"_s_"+name+'.obj'
    #destination_path = wpath+'/'+ folder +'/'+prefix+newname+'.obj'
    if os.path.isfile(src_path):
        copy(src_path, destination_path)
    else:
        print("couldnt find "+ src_path)



# 'F.geojson'
with open('F_quarter.geojson', 'r') as file:
    data = json.load(file)
    for f in data["features"]:
        n = f["properties"]["name"].split("|")
        names.append(str(n[0]).replace(" ",""))
        newnames.append(str(n[1]).replace(" ",""))



c = 0
for n in names:
    add = n.split("_")
    bigtile = (int(add[0]),int(add[1]))
    #postprocessHmap.closegaps((int(add[0]),int(add[1])))
    #print("{"+ str(add[0])+","+str(add[1])+"},")
    #segmentSatImage.segment(n)
    print(n)
    #overpassQuery.cropGeoJsonPoly(bigtile,'austriaShapefiles/austria_roads-smoothed_1.geojson','roadssmooth')
    #landuse.makeMasksfromLanduse(bigtile)
    src_path = n +'/'+"roads_"+n+'.obj'
    destination_path = 'worldmachine_json/newroads/rw_'+newnames[c]+'.obj'

    makeLakes.makeRoadMesh(n)
    copyfiles(src_path,destination_path)
    #thermalcalculator.searchCountures(bigtile)

    c += 1
    '''
    Mask = np.zeros( (2041,2041,1), dtype=np.uint8)
    riversmask = masks.drawLines(10, bigtile, "rivers_", Mask)
    areal = masks.drawLines(6, bigtile, "aerialways_", riversmask)
    powerlines = masks.drawLines(5, bigtile, "power_", areal)
    buildings = masks.drawLines(5, bigtile, "buildings_", powerlines)
    cv2.imwrite(n+'/fmask'+n+'.png', buildings)
    
    #makeBuildingGeometry.makeBuildings(n)
    bigtile = (int(add[0]),int(add[1]))
    try:
        masks.drawLinesRoads(bigtile)
    except:
        print("err")
        print(bigtile)
    #
    
    postprocessHmap.closegaps(bigtile)
      
    #makeLakes.makeLakesMesh(n)
    image = cv2.imread(n +'/'+"hmap_burnIn_"+n+'.png', cv2.IMREAD_UNCHANGED)
    # Loading the image
    half = cv2.resize(image, (505, 505), interpolation = cv2.INTER_LINEAR)
    cv2.imwrite(n +'/'+"hmap_burnIn_quarter_"+n+'.png', half)
    
   
    src_path = n +'/'+"building_s_"+n+'.obj'
    destination_path = wpath+'/building/b_'+newnames[c]+'.obj'
    copyfiles(src_path,destination_path)
    c += 1
    
    
    src_path = n +'/'+"lakes_"+n+'.obj'
    destination_path = wpath+'/lakes/lakes_'+newnames[c]+'.obj'
    copyfiles(src_path,destination_path)

    src_path = n +'/'+"thermals_"+n+'.json'
    destination_path = wpath+'/thermals/thermal_'+newnames[c]+'.json'
    copyfiles(src_path,destination_path)

    
    src_path = n +'/'+"communication_towers_"+n+'.json'
    destination_path = wpath+'/comtower/com_'+newnames[c]+'.json'
    copyfiles(src_path,destination_path)

    src_path = n +'/'+"runways_"+n+'.json'
    destination_path = wpath+'/runways/runway_'+newnames[c]+'.json'
    copyfiles(src_path,destination_path)

    src_path = n +'/'+"windturbines_"+n+'.json'
    destination_path = wpath+'/windturbines/win_'+newnames[c]+'.json'
    copyfiles(src_path,destination_path)
    
    src_path = n +'/'+"aerialways_"+n+'.json'
    destination_path = wpath+'/aerialways/aerialway_'+newnames[c]+'.json'
    copyfiles(src_path,destination_path)
    
    src_path = n +'/'+"lakesReady_"+n+'.json'
    destination_path = wpath+'/lakes/lakes_'+newnames[c]+'.json'
    copyfiles(src_path,destination_path)
       
    #overpassQuery.cropGeoJsonPoly(bigtile,'geojson_src/aerialways.geojson','aerialways')
    #overpassQuery.cropGeoJsonPoly(bigtile,'geojson_src/communication_towers.geojson','communication_towers')
    #overpassQuery.cropGeoJsonPoly(bigtile,'geojson_src/windturbines.geojson','windturbines')
    #overpassQuery.cropGeoJsonPoly(bigtile,'geojson_src/thermals.geojson','thermals')
    #makeLakes.makeLakes(n)
    #makeBuildingGeometry.filterBuildings(n)
    #
    #copyfiles(n,newnames[c],"worldmachine_json")

    
    
### create items if they dont exist
    path = n+"/hmap"+n+".png"
    #path = n+"/landscape.stl"
    if os.path.isdir(n):
        if os.path.isfile(path):
            #print("{"+ str(add[0])+","+str(add[1])+"},")

            print(n)
            c += 1
            #makeLakes.cropGeoJsonLineFeature(n)
            #
            
            try:
                alt = cv2.imread(path, cv2.IMREAD_UNCHANGED) #, cv2.IMREAD_GRAYSCALE
                cv2.imwrite(n+"/nmap_small_"+n+".png", normalfromhightmap.makeNormalmap(alt))
                
                #makeBuildingGeometry.makeBuildings(n)
                #makeLandscapeMesh.createMesh(n)
                #makeLakes.makeRoadMesh(n)
                #makeLakes.makeRiverMesh(n)
            except:
                print(n +" something went wrong")
           # makeLakes.makeLakes(n)
           

#print(str(c) +"x not found")
'''  