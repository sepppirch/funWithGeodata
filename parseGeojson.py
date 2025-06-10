
import geopandas as gpd
import json
'''
gj = gpd.read_file('buildings_werfenJSON.geojson', driver='GeoJSON')
print(gj.head())


for row in gj:
    print(row["geometry"])
'''


 
# Opening JSON file
f = open('buildings_werfenJSON.geojson')
 
# returns JSON object as
# a dictionary
data = json.load(f)


for i in data["features"]:
    for j in range(len(i["geometry"]["coordinates"][0][0])): #["properties"]
        print(i["geometry"]["coordinates"][0][0][j])