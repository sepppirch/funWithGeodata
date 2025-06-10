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


def makeNormalmap(bigtile, size):
#print(alt)
    ksize = (8, 8)
    name = str(bigtile[0])+"_"+str(bigtile[1])
    # Using cv2.blur() method 
    #alt = cv2.blur(alt, ksize)
    alt = cv2.imread(name +'/hmap'+ name+'.png',cv2.IMREAD_UNCHANGED )
    alt = cv2.resize(alt, (size,size), interpolation = cv2.INTER_AREA) 
    w= alt.shape[0]
    h= alt.shape[1]
    normal = np.zeros((h,w,3), np.uint8)

    for i in range(w-1):
        for j in range(h-1):
            

            normal[i,j] = (alt[i,j],0,0)
            xx = 1
            A = np.array([0,0, alt[i,j] * 1.5625*xx])
            B = np.array([200,0, alt[i+1,j] * 1.5625*xx])
            C = np.array([0,200, alt[i,j+1] * 1.5625*xx])
            
            V1 = np.subtract(A,B)
            V2 = np.subtract(A,C)

            #print(np.cross(V1, V2))
            #print(alt[i,j])
            nvec = np.cross(V1, V2)
            l = np.linalg.norm(nvec)
            nvec = nvec/l*90
            nvec1 = np.add(nvec,[128,128,128])
            #print(nvec1)
            normal[i,j] = nvec1

    for i in range(w):
        normal[i,h-1] = normal[i,h-2]
    for i in range(w):
        normal[w-1,i] = normal[w-2,i]

    
    cv2.imwrite(name+"/nmap_small_"+name+".png", normal)



def downloadSat(bigtile, zoom):
    name = str(bigtile[0])+"_"+str(bigtile[1])
    if os.path.exists(name + '/sat_'+ str(zoom) +name+'.jpg'):
        print("sat image exist, skipping")
    else:
        with open(os.path.join(file_dir, 'preferences.json'), 'r', encoding='utf-8') as f:
            prefs = json.loads(f.read())

        if not os.path.isdir(prefs['dir']):
            os.mkdir(prefs['dir'])

        if (prefs['tl'] == '') or (prefs['br'] == '') or (prefs['zoom'] == ''):
            messages = ['Top-left corner: ', 'Bottom-right corner: ', 'Zoom level: ']
            inputs = [0,0,16]#take_input(messages)
            if inputs is None:
                return
            else:
                prefs['tl'], prefs['br'], prefs['zoom'] = inputs
    #DON'T CHANGE THIS!!!
        center = (47.48802456352513, 13.233287974359211)
        h=0.1096
        w=0.16
        
        topLeft = (center[1] + bigtile[1] * w, center[0] - bigtile[0] * h)
        bottomRight = (topLeft[0]+ w, topLeft[1]- h)
        name = str(bigtile[0])+"_"+str(bigtile[1])
        

            
        # download Sat IMAGE
        #zoom = int(prefs['zoom'])
        
        lat1 = float(topLeft[1])
        lon1 = float(topLeft[0])
        lat2 = float(bottomRight[1])
        lon2 = float(bottomRight[0])
        if prefs['tile_format'].lower() == 'png':
            channels = 4
        else:
            channels = 3    
        img = download_image(lat1, lon1, lat2, lon2, zoom, "https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",prefs['headers'], prefs['tile_size'], channels)  
        #newsize = (512,512)
        #img = cv2.resize(img, newsize, interpolation = cv2.INTER_AREA)
        cv2.imwrite(name + '/sat_z'+ str(zoom) +name+'.jpg', img) 
        print(img.shape)


def downloadSat2():
    

    with open(os.path.join(file_dir, 'preferences.json'), 'r', encoding='utf-8') as f:
        prefs = json.loads(f.read())

    if not os.path.isdir(prefs['dir']):
        os.mkdir(prefs['dir'])

    if (prefs['tl'] == '') or (prefs['br'] == '') or (prefs['zoom'] == ''):
        messages = ['Top-left corner: ', 'Bottom-right corner: ', 'Zoom level: ']
        inputs = [0,0,16]#take_input(messages)
        if inputs is None:
            return
        else:
            prefs['tl'], prefs['br'], prefs['zoom'] = inputs
 
    center = (47.48802456352513, 13.233287974359211)
    h=0.1096
    w=0.16
    
    topLeft = (center[1] - w * 10, center[0] + 4 * h)
    bottomRight = (topLeft[0]+ w*18, topLeft[1]- h*18)
 
    

        
    # download Sat IMAGE
    zoom = int(prefs['zoom'])
    zoom = 12
    lat1 = float(topLeft[1])
    lon1 = float(topLeft[0])
    lat2 = float(bottomRight[1])
    lon2 = float(bottomRight[0])
    if prefs['tile_format'].lower() == 'png':
        channels = 4
    else:
        channels = 3    
    img = download_image(lat1, lon1, lat2, lon2, zoom, "https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",prefs['headers'], prefs['tile_size'], channels)  
    newsize = (4096,4096)
    #img = cv2.resize(img, newsize, interpolation = cv2.INTER_AREA)
    cv2.imwrite('satEz13.jpg', img) 
    print(img.shape)

#downloadSat((11,3),13)
    
#makeNormalmap((0,0),256)




