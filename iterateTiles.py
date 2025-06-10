import createTile
#import hightmapTiles
import postprocessHmap
import os

for x in range (-1,17):  #horizontal
    for y in  range(18,23):
        #bigtile = (y-1+6,x-4-9)
        bigtile = (x,y)
        #
        #postprocessHmap.closegaps(bigtile)
        #hightmapTiles.subtractRoadMask(bigtile)
        if not os.path.isdir(str(bigtile[0]) +"_"+str(bigtile[1])):
            print(bigtile)
            createTile.createATile(bigtile)
        
        #if bigtile[1] > -17:
            
            

