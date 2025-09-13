from geotiff import GeoTiff
import numpy as np
from PIL import Image, ImageFilter


#tiff_file = "eu_dem_v11_E40N20.TIF"
#geo_tiff = GeoTiff(tiff_file, crs_code=3035, as_crs=4258)#4258




def makeMasksfromLanduse(bigtile):
    name = str(bigtile[0])+"_"+str(bigtile[1])
    newsize = (2041, 2041)
    try:
        tiff_file = "landuse/landuse.tif"

        geo_tiff = GeoTiff(tiff_file, crs_code=4326, as_crs=4326)#4258

        
        hmap = Image.open(name+"/hmap"+name+".png")
        hmd = hmap.getdata()
        #print(hmd[1])

        nmap =  Image.open(name+"/nmap_small_"+name+".png")
        red, green, blue = nmap.split()
        nmap = red.resize(newsize, Image.Resampling.BILINEAR)
        #nmap.show()
        nmd = nmap.getdata()

        roadsmask = Image.open(name+"/rmask"+name+".png")
        rmb = roadsmask.filter(ImageFilter.BoxBlur(0.5))
        roadsmask = rmb.point( lambda p: 255 if p > 17 else 0 )
        rmdata = roadsmask.getdata()
        #roadsmask.show()
        grassmask = Image.open(name+"/grassn"+name+".png") 
        gmd = grassmask.getdata()

        forestmask = Image.open(name+"/fmask"+name+".png") 
        fmd = forestmask.getdata()

        icemask =  Image.open(name+"/ice"+name+".png")
        imd = icemask.getdata() 
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
        #print(array)
        # reshape to 2d#mat = np.reshape(array,(256,256))
        # Creates PIL image
        #img = Image.fromarray(np.uint8(array/20) , 'L')
        #img.show()
        #img.save('foo.png')

        lusemap = Image.fromarray(np.uint8(array)) # or more verbose as Image.fromarray(ar32, 'I')

        
        lum = lusemap.resize(newsize, Image.Resampling.NEAREST)

        #lusemap.save(name +'/height.png')
        #nm.save(name+'/luse_'+name+'.png')
        #print(nm)
        #this exports a 16bit png for lanscape in ue4

        

        newimdata = []
        allcolors = []
        

        i = 0
        for color in lum.getdata():
            if color not in allcolors:
                allcolors.append(color)
            # hmd[i] < (17000 + (nmd[i]-140) * 60) -- randomize treeline to avoid a straight line
            if rmdata[i] < 20 and color == 2 and gmd[i] < 128 and nmd[i] > 150 and fmd[i] < 10 and imd[i] < 20 and hmd[i] < (17000 + (nmd[i]-140) * 50):
                newimdata.append(255)
            else:
                newimdata.append(0)
            i += 1
            #print(i)
        newim = Image.new('L',newsize)
        newim.putdata(newimdata)
        nib = newim.filter(ImageFilter.BoxBlur(1))
        #nib2 = nib.point( lambda p: 255 if p > 10 else 0 )
        nib.save(name + '/forest'+name+'.png')
        

        

        roadsmask = Image.open(name+"/roadsmask"+name+".png")
        rmb = roadsmask.filter(ImageFilter.BoxBlur(0.5))
        roadsmask = rmb.point( lambda p: 255 if p > 15 else 0 )
        
        rmdata = roadsmask.getdata()

        
        newimdata = []
        allcolors = []
        
        i = 0
        for color in lum.getdata():
            if color not in allcolors:
                allcolors.append(color)
            # hmd[i] < (17000 + (nmd[i]-140) * 60) -- randomize treeline to avoid a straight line
            if  (color == 5 or color == 7 or color == 11 or gmd[i] > 128) and rmdata[i] < 2 and nmd[i] > 155 and imd[i] < 20 and hmd[i] < (17000 + (nmd[i]-140) * 60):
                newimdata.append(255)
            else:
                newimdata.append(0)
            i += 1
            #print(i)
        newim = Image.new('L',newsize)
        newim.putdata(newimdata)
        nib = newim.filter(ImageFilter.BoxBlur(1))
        nib2 = nib.point( lambda p: 255 if p > 100 else 0 )
        nib2.save(name + '/grass'+name+'.png')
        #nib2.show()
        
        '''
        newimdata = []
        allcolors = []
        
        i = 0
        for color in lum.getdata():
            if color not in allcolors:
                allcolors.append(color)
            
            if color == 9 and nmd[i] > 160 :
                newimdata.append(255)
            else:
                newimdata.append(0)
            i += 1
            #print(i)

        newimdata = []
        
        newimage = Image.open(name+"/rmask"+name+".png")
        #newimage.show()
        
        #newimdata.putdata(newimage)
        nib = newimage.filter(ImageFilter.BoxBlur(0.1))
        nib2 = nib.point( lambda p: 255 if p > 100 else 0 )
        nib2.save(name + '/asphalt'+name+'.png')
        #nib2.show()
        

        newimdata = []
        allcolors = []
        



        # grassmap: invert forest and subtrakt others
        forestmask = Image.open(name+"/forest"+name+".png") 
        fmd = forestmask.getdata()
        asphaltmask = Image.open(name+"/asphalt"+name+".png") 
        amd = forestmask.getdata()
        fieldsmask = Image.open(name+"/fields"+name+".png") 
        cmd = fieldsmask.getdata()
        snowmask = Image.open(name+"/ice"+name+".png") 
        imd = fieldsmask.getdata()
        
        
        

            #print(i)
        # 0 = ?
        # 1 = water == rocks
        # 2 = forest
        # 3 = ?
        # 4 = ?
        # 5 = fields
        # 6 = ?
        # 7 = builtArea/Asphalt + roadsmask
        # 8 = rocks
        # 9 = ice
        # 10 = ?
        # 11 = grassland 
        '''
        
    except:
        print("no landuse map - fallback")
        im = Image.open(name + "/grassn"+ name + ".png")
        im.save(name + '/fields'+name+'.png')

        im = Image.open(name + "/forestn"+ name + ".png")
        im.save(name + '/forest'+name+'.png')

        im = Image.open(name + "/roadsmask"+ name + ".png")
        im.save(name + '/asphalt'+name+'.png')

        im = Image.new(mode="L", size=(2041, 2041))
        im.save(name + '/grass'+name+'.png')
        im.save(name + '/ice'+name+'.png')


#makeMasksfromLanduse((3,-4))

        
