import os
import json
import re
import cv2
from datetime import datetime
import math
from image_downloading import download_image
from geotiff import GeoTiff
import numpy as np
from PIL import Image, ImageFilter



file_dir = os.path.dirname(__file__)
prefs_path = os.path.join(file_dir, 'preferences.json')
default_prefs = {
        'url': 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        #'url': 'https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        'tile_size': 256,
        'tile_format': 'jpg',
        'dir': os.path.join(file_dir, 'images'),
        'headers': {
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        },
        'tl': '',
        'br': '',
        'zoom': ''
    }

def makeRGBHmap(path,tilesSqr):
    alt16 = cv2.imread(path +'/height.png', cv2.IMREAD_UNCHANGED)
    height = alt16.shape[0]
    width = alt16.shape[1]
    
     
    hmaprgb = Image.new('RGB', (tilesSqr*64, tilesSqr*64))
    #pixels = bigpictureN.load()
    for x in range(width):
        for y in range(height):
            
            val = alt16[y][x]
            r = math.floor(val%256)
            g = math.floor(val/256)
            hmaprgb.putpixel((x, y), (r,g,0)) 

    hmaprgb.save(path +'/alt.png')
    hmaprgb.close()


def makeNormalmap(path):
#print(alt)
    ksize = (8, 8)
    alt = cv2.imread(path +'/height.png', cv2.IMREAD_UNCHANGED)
    # Using cv2.blur() method 
    alt = cv2.blur(alt, ksize)
    w= alt.shape[0]
    h= alt.shape[1]
    normal = np.zeros((h,w,3), np.uint8)

    for i in range(w-1):
        for j in range(h-1):
            

            normal[i,j] = (alt[i,j],0,0)
            A = np.array([0,0,alt[i,j]])
            B = np.array([1,0,alt[i+1,j]])
            C = np.array([0,1,alt[i,j+1]])
            
            V1 = np.subtract(A,B)
            V2 = np.subtract(A,C)

            #print(np.cross(V1, V2))
            #print(alt[i,j])
            nvec = np.cross(V1, V2)
            l = np.linalg.norm(nvec)
            nvec = nvec/l*100
            nvec1 = np.add(nvec,[128,128,128])
            #print(nvec1)
            normal[i,j] = nvec1

    for i in range(w):
        normal[i,h-1] = normal[i,h-2]
    for i in range(w):
        normal[w-1,i] = normal[w-2,i]

    cv2.imwrite(path +"/nmap.png", normal)
    return normal



def run():
    with open(os.path.join(file_dir, 'preferences.json'), 'r', encoding='utf-8') as f:
        prefs = json.loads(f.read())

    if not os.path.isdir(prefs['dir']):
        os.mkdir(prefs['dir'])

    if (prefs['tl'] == '') or (prefs['br'] == '') or (prefs['zoom'] == ''):
        messages = ['Top-left corner: ', 'Bottom-right corner: ', 'Zoom level: ']
        inputs = [0,0,17]#take_input(messages)
        if inputs is None:
            return
        else:
            prefs['tl'], prefs['br'], prefs['zoom'] = inputs

    bigtile = (0,1)
    downloadSatImg = False
    #center = (47.48802456352513, 13.233287974359211)
    #DON'T CHANGE THIS!!!
    # https://www.opendem.info/opendemeu_download_4258.html  hightmaps here!!!
    size = 0.1
    center = (47.48802456352513, 13.233287974359211)
    #DON'T CHANGE THIS!!!
    name = str(bigtile[0])+"_"+str(bigtile[1])
    
    # stitch tiles for sat and alt images together

    try:
        os.mkdir(name)


        #tiff_file = "eu_dem_v11_E40N20.TIF"

        #geo_tiff = GeoTiff(tiff_file, crs_code=3035, as_crs=4258)#4258,3857
        #convertedAlpsdem.tif
        tiff_file = "alpsHigher.tif"
        geo_tiff = GeoTiff(tiff_file, crs_code=4258, as_crs=4258)#4258
        tilesSqr = 8
        sattexsize = 1024
        bighmap = Image.new('I', (tilesSqr*64, tilesSqr*64))
        bigpictureSat = Image.new('RGB', (tilesSqr*sattexsize, tilesSqr*sattexsize))

        for x in range(tilesSqr):
            for y in range(tilesSqr):
        #center = (46.257023492840055 + 0.0685 * size * 2 , 13.678651478956224)
            
                xoffset = 0.0685 * size * 2 * x + 0.0685 * size * 2 * tilesSqr * bigtile[0]
                yoffset = 0.1 * size * 2 * y + 0.1 * size * 2 * tilesSqr * bigtile[1]

                #topLeft = (center[0] + 0.0685 * size - xoffset , center[1] - 0.1 * size + yoffset)
                topLeft = (center[0] - xoffset , center[1] + yoffset)
                ##topLeft  = (47.137, 12.4)
                bottomRight= (center[0] - 0.0685 * size * 2 - xoffset , center[1] + 0.1 * size * 2 + yoffset)
                #bottomRight =(47.0, 12.6)

        
            


                #img = download_image(lat1, lon1, lat2, lon2, zoom, "https://tile.openstreetmap.org/{z}/{x}/{y}.png",prefs['headers'], prefs['tile_size'], channels)
                #cv2.imwrite(name + '/topo.png', img)
                #print(f'Saved as {name}')
                


                #print(geo_tiff.tif_bBox)
                # in WGS 84 coords
                #print(geo_tiff.tif_bBox_converted)
                #zarr_array = geo_tiff.read()



                # in WGS 84
                area_box = [(topLeft[1], topLeft[0]), (bottomRight[1], bottomRight[0])]
                #geo_tiff = GeoTiff(tiff_file)
                array = geo_tiff.read_box(area_box)

                # Creates PIL image
                #img = Image.fromarray(np.uint8(array/20) , 'L')
                img = Image.fromarray(np.uint32(array), "I")
                #img.show()
                #img.save('height.png')

                width, height = img.size
                print(img.size)

                '''
                if width < height:
                    img = img.crop((0, 0, width, width))
                else:
                    img = img.crop((0, 0, height, height))
                '''
                newsize = (64, 64)
                img = img.resize(newsize, Image.Resampling.BICUBIC)
                
                bighmap.paste(img, (y*64, x*64))
                #print(bigpicture[0][0])
                
                #bigpicture.save('height.png')
                #img.save(name + '/alt'+str(x)+'_'+str(y)+'.png')
                

                if downloadSatImg:

                    zoom = int(prefs['zoom'])
                    lat1 = float(topLeft[0])
                    lon1 = float(topLeft[1])
                    lat2 = float(bottomRight[0])
                    lon2 = float(bottomRight[1])
                    if prefs['tile_format'].lower() == 'png':
                        channels = 4
                    else:
                        channels = 3

                    img = download_image(lat1, lon1, lat2, lon2, zoom, "https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",prefs['headers'], prefs['tile_size'], channels)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    im_pil = Image.fromarray(img)
                    im_pil = im_pil.resize((sattexsize,sattexsize),Image.Resampling.BOX)
                    bigpictureSat.paste(im_pil, (y*sattexsize, x*sattexsize))
                    #sqsize = 0
                    #if img.shape[0]>img.shape[1]:
                        #sqsize = img.shape[1]
                    #else:
                        #sqsize = img.shape[0]
                    #img.resize((sqsize, sqsize))
                    #cropped_image = img[0:0, 512:512]
                    #cv2.imwrite(name + '/sat.jpg', img)

                    #cropped_image = img[0:sqsize, 0:sqsize]
                    #cv2.imwrite(name + '/satcropped.jpg', cropped_image)
                    print(img.shape)

            
        
        
        # Using cv2.blur() method 
        #blur = bigpicture.filter(ImageFilter.GaussianBlur(radius = 2))
         
        if downloadSatImg:
            bigpictureSat.save(name +'/sat.jpg')
            bigpictureSat.close()
        #16bit hmap
        
        bighmap.save(name +'/height.png')

        newsize = (568, 568)
        bighmap = bighmap.resize(newsize, Image.Resampling.BICUBIC)


        newimdata = []

        for color in bighmap.getdata():
            newimdata.append(color*10)

        newim = Image.new('I',bighmap.size)
        newim.putdata(newimdata)

        newim.save(name +'/heightUE4.png')
        
        bighmap.close()
        
        '''
        makeRGBHmap(name,8)
        alt = cv2.imread(name +'/height.png', cv2.IMREAD_UNCHANGED)
        cv2.imwrite(name +"/nmap.png", makeNormalmap(alt))
        
        px = bighmap.load()
        hmaprgb = Image.new('RGB', (tilesSqr*64, tilesSqr*64))
        #pixels = bigpictureN.load()
        for x in range(tilesSqr*64):
            for y in range(tilesSqr*64):
                
                val = px[x,y]
                r = math.floor(val%256)
                g = math.floor(val/256)
                hmaprgb.putpixel((x, y), (r,g,0)) 
    
        hmaprgb.save(name +'/alt.png')
        '''

    except OSError as error:
        print(error) 

    



if os.path.isfile(prefs_path):
    run()

else:
    with open(prefs_path, 'w', encoding='utf-8') as f:
        json.dump(default_prefs, f, indent=2, ensure_ascii=False)

    print(f'Preferences file created in {prefs_path}')
