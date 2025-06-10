import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle



center = (47.48802456352513, 13.233287974359211)

#bbox=( 13.5, 46.6, 13.6, 46.5)
h=0.1096
w=0.16
bbox=(center[1],center[0],center[1]+w,center[0]-h)
gdf = gpd.read_file(
    'austriaShapefiles/gis_osm_landuse_a_free_1.shp',
    bbox=bbox,
)

#filtered =  gdf[gdf.name == "residential"]

#print(filtered)
'''
for feature in gdf.columns:
    print(feature)
'''    


g = gdf.groupby('fclass')

print(g.groups.keys())


#shape=gpd.read_file('power_alps.shp')  austriaShapefiles/gis_osm_roads_free_1.shp
#EPSG:4326
gdf.crs = "EPSG:4326"
gdf.to_crs(epsg=4258)
#gdf.plot(linewidth=0.1)
filtered = gdf.groupby('fclass').get_group('grass')# meadow forest scrub
filtered1 = gdf.groupby('fclass').get_group('forest')# meadow forest scrub
#gdf.plot()

filtered1.plot(linewidth=0.1, color=(0.0, 1.0, 0))

#plt.margins(x=0)
plt.axis('off')
#plt.tight_layout()


ax = plt.gca()
ax.add_patch(Rectangle((center[1], center[0]), 0.02, 0.02, alpha=1))
ax.add_patch(Rectangle((center[1] + w, center[0]- h), 0.02, 0.02,alpha=1))

plt.xlim([center[1]-0.02, center[1]+w+0.02])
#plt.ylim([47.375,47.5])
plt.ylim([center[0]-h-0.02 ,center[0]+0.02])




'''
plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)


'''
plt.margins(0,0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.savefig('match.png', dpi=1800)
plt.show()