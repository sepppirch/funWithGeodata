from geotiff import GeoTiff
import numpy as np
from PIL import Image


#tiff_file = "eu_dem_v11_E40N20.TIF"
#geo_tiff = GeoTiff(tiff_file, crs_code=3035, as_crs=4258)#4258

tiff_file = "alpsHigher.tif"
geo_tiff = GeoTiff(tiff_file, crs_code=4258, as_crs=4258)#4258

bigtile = (0,0)

name = str(bigtile[0])+"_"+str(bigtile[1])
#print(geo_tiff.tif_bBox)
# in WGS 84 coords
#print(geo_tiff.tif_bBox_converted)
#zarr_array = geo_tiff.read()


    #center = (47.48802456352513, 13.233287974359211)
    #DON'T CHANGE THIS!!!
    # https://www.opendem.info/opendemeu_download_4258.html  hightmaps here!!!
center = (47.48802456352513, 13.233287974359211)

h=0.1096
w=0.16
#DON'T CHANGE THIS!!!
topleft = (center[1] + bigtile[1] * w, center[0] - bigtile[0] * h)
area_box = [(topleft[0],topleft[1]), (topleft[0]+w,topleft[1]-h)]

array = geo_tiff.read_box(area_box)
print(array.shape)
# reshape to 2d#mat = np.reshape(array,(256,256))
# Creates PIL image
#img = Image.fromarray(np.uint8(array/20) , 'L')
#img.show()
#img.save('foo.png')

hmap = Image.fromarray(np.uint32(array), "I") # or more verbose as Image.fromarray(ar32, 'I')

newsize = (1017, 1017)
bighmap = hmap.resize(newsize, Image.Resampling.BICUBIC)
newimdata = []

bighmap.save(name +'/height.png')
#this exports a 16bit png for lanscape in ue4
for color in bighmap.getdata():
    newimdata.append(color*10)
newim = Image.new('I',bighmap.size)
newim.putdata(newimdata)
newim.save(name + '/heightUE4.png')

bighmap.close()