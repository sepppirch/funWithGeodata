import cv2
import os
import segmentSatImage

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])


for u in range (4):
    for v in range (0,2):
        bt=[u,v]
        moreImages = []
        moreImages1 = []
        offset = [35 -bt[1]*9,-58 + bt[0]*9]

        for y in range(9):
            images = []
            images1 = []
            for x in range (9):
            #for x in range (-4,5):
                #name = str(y-1)+"_"+str(x-31)
                

                name = str(y + offset[0])+"_"+str(x + offset[1])
                #str(y)+"_"+str(x)
                path = name + "/hmap_burnIn_"+name
                if os.path.isfile(path): 
                    forest = cv2.imread(name+'/forestn'+name+'.png', cv2.IMREAD_UNCHANGED)
                    grass = cv2.imread(name+'/grassn'+name+'.png', cv2.IMREAD_UNCHANGED)
                    #im1 = cv2.resize(im1, dsize=(0, 0), fx=0.1, fy=0.1)
                    #im1 = cv2.imread(name+'/hmap'+name+'.png', cv2.IMREAD_UNCHANGED)
                    im1 = cv2.imread(name+'/roadsmask'+name+'.png', cv2.IMREAD_UNCHANGED)
                    #im1 = cv2.resize(im1, dsize=(0, 0), fx=0.25, fy=0.25)
                    im2 = cv2.imread(name+'/rocksn'+name+'.png', cv2.IMREAD_UNCHANGED)
                    rocks = cv2.add(im1, im2)
                    #im1 = cv2.imread(name+'/hmap'+name+'.png', cv2.IMREAD_UNCHANGED)
                    im1 = cv2.imread(name+'/rivers'+name+'.png', cv2.IMREAD_UNCHANGED)
                    #im1 = cv2.resize(im1, dsize=(0, 0), fx=0.25, fy=0.25)
                    im2 = cv2.imread(name+'/lake'+name+'.png', cv2.IMREAD_UNCHANGED)
                    water = cv2.bitwise_not(cv2.add(im1, im2))
                    img8 = (water/256).astype('uint8')
                    #im2 = cv2.resize(im1, dsize=(0, 0), fx=0.25, fy=0.25)
                    im3 =  cv2.merge([forest, grass, rocks,img8]) 
                    images.append(im3) 
                    
                    hm = cv2.imread(name+'/hmap_burnIn_'+name+'.png', cv2.IMREAD_UNCHANGED)
                    #hm = cv2.resize(hm, dsize=(0, 0), fx=0.1, fy=0.1)
                    images1.append(hm)

                else:
                    #segment images
                    segmentSatImage.segmentSimple(name)

                    forest = cv2.imread(name+'/forestn'+name+'.png', cv2.IMREAD_UNCHANGED)
                    grass = cv2.imread(name+'/grassn'+name+'.png', cv2.IMREAD_UNCHANGED)
                    rocks = cv2.imread(name+'/rocksn'+name+'.png', cv2.IMREAD_UNCHANGED)

                    im3 =  cv2.merge([forest, grass, rocks]) 
                    images.append(im3) 
                    path = name + "/hmap_"+name+'.png'
                    if os.path.isfile(path):
                        hm = cv2.imread(name+'/hmap_'+name+'.png', cv2.IMREAD_UNCHANGED)
                    path = name + "/hmap"+name+'.png'
                    if os.path.isfile(path):
                        hm = cv2.imread(name+'/hmap'+name+'.png', cv2.IMREAD_UNCHANGED)
                    #hm = cv2.resize(hm, dsize=(0, 0), fx=0.1, fy=0.1)
                    images1.append(hm)

            moreImages.append(images)
            moreImages1.append(images1)

        btname = "X"+str(bt[0])+"_Y"+str(bt[1])
        im_tile = concat_tile(moreImages)
        im_tile = cv2.resize(im_tile, (4096,4096), interpolation= cv2.INTER_LINEAR)
        cv2.imwrite('9x9_tiles/mask/m_'+btname+'.png', im_tile)

        im_tile1 = concat_tile(moreImages1)
        im_tile1 = cv2.resize(im_tile1, (1017,1017), interpolation= cv2.INTER_LINEAR)
        cv2.imwrite('9x9_tiles/hmap/h_'+btname+'.png', im_tile1)