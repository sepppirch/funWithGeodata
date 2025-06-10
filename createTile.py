import downloadSatImage
import overpassQuery
import segmentSatImage
import hightmapTiles
import hightmapTilesSwiss
import makeLakes
import os
import makeBuildingGeometry
import makeLandscapeMesh
import findConnectedRoads
import json

def createATile (bigtile):
    name = str(bigtile[0])+"_"+str(bigtile[1])
    
    try:
        os.mkdir(name)

    except OSError as error:
        print("directory exists")
    '''
    overpassQuery.cropGeoJsonPoly(bigtile,'runways.geojson','runway')
    overpassQuery.cropGeoJsonPoly(bigtile,'aerialways.geojson','aerialways')
    '''
    downloadSatImage.downloadSat(bigtile,12)
    #makeBuildingGeometry.makeBuildings(name)

    '''
    #segmentSatImage.segment(name)
    overpassQuery.downloadGeoJson(bigtile,'way["building"]',"LineString", 'buildings')
    overpassQuery.downloadGeoJson(bigtile,'way["highway"]',"LineString", 'roads')
    overpassQuery.cropGeoJsonPoly(bigtile,'alpsGeoJSON/alps_lakes_sp.geojson','lakes')
    overpassQuery.cropGeoJsonPoly(bigtile,'alpsGeoJSON/alps_rivers_sp.geojson','rivers')
    
    overpassQuery.downloadGeoJson(bigtile,'way[waterway=river]',"LineString", 'rivers')
    overpassQuery.cropGeoJsonPoly(bigtile,'talwind.geojson','talwind')
    overpassQuery.downloadGeoJson(bigtile,'node[natural=peak]',"Point", 'peaks')
    overpassQuery.downloadGeoJson(bigtile,'way[power=line]',"LineString", 'power')
    f = open(name+'/rivers_'+name+'.json')
    data = json.load(f)
    
    outfilename = "riversMerged"
    with open(name +"/"+ outfilename +"_"+name+".json",mode="w") as f:
        json.dump(findConnectedRoads.combineMultiSegmentLines(data),f) 
    if bigtile[1] < -18 and bigtile[0] > -2 :
        hightmapTilesSwiss.makeHightMap(bigtile)
    else:
        hightmapTiles.makeHightMap(bigtile)
    #makeLakes.cropGeoJsonLineFeature(name)
    #   
     
    hightmapTiles.hightmapBurnIn(bigtile)
    
    makeLakes.makeLakes(name)
    #
    #
    #
    #makeLandscapeMesh.createMesh(name)
    segmentSatImage.segment(name)

#   '''
    
     
    hightmapTiles.makeHightMap(bigtile)
         
    #hightmapTiles.hightmapBurnIn(bigtile)
    #makeLakes.makeRiverMesh(name)
    #makeLakes.makeRoadMesh(name)
    #downloadSatImage.makeNormalmap(bigtile, 256)
#createATile((-1,-50))

#hightmapTiles.makeHightMap((52,-49))