import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import pandas as pd
import cv2
import math
import numpy as np

def readSHP(path):
    shp = gpd.read_file(
        path,
        bbox=bbox,
    )

    shp.crs = "EPSG:4326"
    shp.to_crs(epsg=4258)

    g = shp.groupby('fclass')
    #0,109
    return shp, g.groups.keys()

def searchandPlot(shp, keys, terms, linew, col):
    for term in terms:
        if term in keys:
            print(str(term) +" found")
            result = shp.groupby('fclass').get_group(term)
            result.plot(ax=ax, linewidth=linew, color=col)
        else:
            print(str(term) +" not found")

# dont change
center = (47.48802456352513, 13.233287974359211)

h=0.1096
w=0.16

bigtile = (-1,-2)
name = str(bigtile[0])+"_"+str(bigtile[1])

#topLeft = (center[0] - xoffset , center[1] + yoffset)
topleft = (center[1] + bigtile[1] * w, center[0] - bigtile[0] * h)
#bottomRight=(center[1] - bigtile[0] * w + w, center[0]- h + bigtile[0] * h)
fig, ax=plt.subplots(figsize=(20,20))
#bbox=(center[1],center[0],center[1]+w,center[0]-h)
bbox=(topleft[0],topleft[1],topleft[0]+w,topleft[1]-h)

waterways, wkeys = readSHP('austriaShapefiles/gis_osm_waterways_free_1.shp')

water, wk = readSHP('austriaShapefiles/gis_osm_water_a_free_1.shp')
watercolor = (0.99, 0.99, 0.99)

searchandPlot(water, wk, ['water','reservoir'], 0.0, watercolor)
searchandPlot(water, wk, ['glacier'], 0.0, (1, 1, 1))
water.plot(ax=ax, linewidth=0.5, color=(0, 0, 1))
#
#waterways.plot(ax=ax, linewidth=0.5, color=(0, 0, 1))
print(wk) 

#searchandPlot(waterways, wkeys, ['river'], 15.0, watercolor)
#searchandPlot(waterways, wkeys, ['stream'], 10.0, watercolor)
#searchandPlot(waterways, wkeys, ['drain'], 2, watercolor)
'''
roads, roadskeys = readSHP('austriaShapefiles/gis_osm_roads_free_1.shp')
roadscolor = (0.0,0.0,0.0)

roads.plot(ax=ax, linewidth=3, color=roadscolor)

searchandPlot(roads, roadskeys, ['motorway','highway_link'], 7, roadscolor)
searchandPlot(roads, roadskeys, ['primary'], 5, roadscolor)


tunnels = gpd.read_file('austriaShapefiles/tunnels2.shp',bbox=bbox)
tunnels.crs = "EPSG:4326"
tunnels.to_crs(epsg=4258)

if len(tunnels['geometry']) > 0:
    tunnelsfiltered = []
    gpd.GeoDataFrame(columns=['id', 'distance', 'feature'], geometry='feature', crs='EPSG:4326')
    #print(tunnels.head())
    for ix, r in tunnels.iterrows():
        if r.geometry.length > 0.001:
            tunnelsfiltered.append(r)

    if len(tunnelsfiltered) > 0:
        gdfTunnels = gpd.GeoDataFrame(tunnelsfiltered)
        gdfTunnels.crs = "EPSG:4326"
        gdfTunnels.to_crs(epsg=4258)
        print(gdfTunnels.head())
        gdfTunnels.plot(ax=ax, linewidth=4, color=(0, 0, 0))       
#res = pd.concat([roads.groupby('fclass').get_group('primary'), roads.groupby('fclass').get_group('residential'), roads.groupby('fclass').get_group('tertiary'), roads.groupby('fclass').get_group('motorway'), roads.groupby('fclass').get_group('primary_link')])

buildings, bkeys = readSHP('austriaShapefiles/gis_osm_buildings_a_free_1.shp')

buildings.plot(ax=ax, color=(0.0, 0.0, 0.0))
print(bkeys)

'''

#res.plot(ax=ax, linewidth=1.2, color=(1, 0, 0))



#roads.plot(ax=ax, linewidth=0.5, color=(1, 0, 0))
#topleft[0],topleft[1],bottomRight[0],bottomRight[1]
#ax.add_patch(Rectangle((center[1], center[0]- 0.002), 0.002, 0.002, alpha=1))
#ax.add_patch(Rectangle((center[1]- 0.002 + w, center[0] - h), 0.002, 0.002, alpha=1))

#ax.add_patch(Rectangle((topleft[0] - 0.001, topleft[1]), 0.001, 0.001, alpha=1,zorder=6,color=(0, 1, 0)))
#ax.add_patch(Rectangle((topleft[0]  + w, topleft[1] - h - 0.001 ), 0.001, 0.001, alpha=1,zorder=6,color=(0, 1, 0)))

ax.add_patch(Rectangle((topleft[0], topleft[1]), w, 0.02, alpha=1,zorder=5,color=(0, 1, 0)))
ax.add_patch(Rectangle((topleft[0], topleft[1] - h - 0.02 ), w, 0.02, alpha=1,zorder=5,color=(0, 1, 0)))

#ax.add_patch(Rectangle((topleft[0], topleft[1]), 0.02, h, alpha=1,zorder=5,color=(0, 1, 0)))
#ax.add_patch(Rectangle((topleft[0]- 0.02, topleft[1] + w), 0.02, h, alpha=1,zorder=5,color=(0, 1, 0)))

#plt.xlim([center[1]-0.00001, center[1]+w+0.00001])
#plt.ylim([center[0]-h-0.00002 ,center[0]+0.00002])
plt.xlim([topleft[0]- 0.001, topleft[0] + w + 0.001])
plt.ylim([topleft[1]- h - 0.0002 , topleft[1] + 0.0002])

#plt.xlim([topleft[0], topleft[0] + w ])
#plt.ylim([topleft[1]- h , topleft[1]])

#topleft[0],topleft[1],bottomRight[0],bottomRight[1]

plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
            hspace = 0, wspace = 0)
plt.margins(0,0)
#plt.axis('off')
##plt.rcParams['axes.facecolor']='black'
plt.rcParams['savefig.facecolor']='black'
plt.savefig(name + '/osm.png', dpi=280, transparent=True)
plt.show()

# crop and rescale osm image

orig = cv2.imread(name + '/osm.png', cv2.IMREAD_UNCHANGED)

dimensions = orig.shape
 
# height, width, number of channels in image
height = orig.shape[0]
width = orig.shape[1]

print(orig[0,1000])
y1 = 0
x1 = 0
for i in range(200):

    if orig[i,1000][1] == 255 and orig[i,1000][0] == 0 and orig[i,1000][2] == 0:  #np.array([0,255,0]):
        y1 = i+1

for i in range(200):
    print(orig[y1-1,i])
    if orig[y1-1,i][3] == 0 :

        x1=i+1
    

print(y1)
print(x1)

cropped_image = orig[y1 : y1 +  height -(y1)*2 , x1 : x1 + width - (x1)*2 ]
square = cv2.resize(cropped_image, (8192, 8192), interpolation = cv2.INTER_CUBIC)
cv2.imwrite( name +'/osm1.png', square)



#cv2.imshow("original", cropped_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# segment Sat image

'''

#alt = cv2.imread(name +'/height.png', cv2.IMREAD_UNCHANGED) #, cv2.IMREAD_GRAYSCALE
sat = cv2.imread(name +'/sat.jpg', cv2.IMREAD_COLOR) #, cv2.IMREAD_GRAYSCALE
osm = square

w= sat.shape[0]
h= sat.shape[1]
segmented = np.zeros((math.floor(h),math.floor(w),3), np.uint8)

#print(alt[0,0])



for i in range(w):
    for j in range(h):
        o = osm[i,j]
        ob = int(o[0]) + int(o[1]) + int(o[2])
        if o[3] < 50 or ob < 50:
            
            c = sat[i,j]
            cb = (int(c[0]) + int(c[1]) + int(c[2]))/3
            green = int(c[1]) /  ((int(c[0]) + int(c[2]) + 1) / 2)
            #th = alt[math.floor(i/16),math.floor(j/16)]
            #print (th)

            #thisalt = 0

            if int(th[0]) > 8:
                thisalt = 3
            elif int(th[0]) > 4:
                thisalt = 2
            elif int(th[0]) > 3:
                thisalt = 1
            else:
                thisalt = 0

          


            
            if green > 1.1:
                if c[1] > 70:  #grass 40 - 55
                    g = 5 * 1 + 40
                    segmented[i,j] = (g,g,g)
                else:          #forest 0 - 15
                    g = 5 * 1
                    segmented[i,j] = (g,g,g)
            
            
            # rocks 70
            elif cb > 100:
                segmented[i,j] = (70,70,70)

        # water 255
        else:
            segmented[i,j] = (o[0],o[1],o[2])
        #streets 128


#cv2.imwrite(name + "/osm1.png", segmented)


'''