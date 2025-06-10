import json
import os
import shutil 
from shutil import copy
import os.path
import makeLakes
import postprocessHmap
#import makeBuildingGeometry
import makeLandscapeMesh
import normalfromhightmap
import cv2
sector = "F"
wpath = "worldmachine_" + sector + "/2041/"
#wpath = "worldmachine_json"


def copyWind(name, newname,dir):
    newpath = r'worldmachine_json/'+dir+'wind/'+dir+'wind__' +newname
    #if not os.path.exists(newpath):
        #os.makedirs(newpath)

    src_dir = name +'/'+dir+'wind'
    files = os.listdir(src_dir)

    shutil.copytree(src_dir, newpath)



def copyfilesForSectors(name, newname, wpath):
    #folders = ["aerialways","bridges","PowerReady","lakes","peaks","talwind"]
    #prefix = ["aerialway_","bridge_","cables_","lakes_","peaks_","talwind_"]
    #folders = ["rivers","roads, building"]
    #prefix = ["river_","rw_","b_"]
    folders = ["forest","grass","ice","asphalt"]
    prefix = ["f_","g_","i_","a_"]
    #folders = ["hmaps"]
    #prefix = ["h_"]
    for i in range (len(folders)):
        wmname = newname.split("_")
        wmname = "X"+str(int(wmname[0].replace("X",""))%18) + "_Y"+ str(int(wmname[1].replace("Y",""))%18)
         
        src_path = name +'/'+folders[i]+name+'.png'
        #if i ==2:
        #src_path = name +'/hmap_burnIn_quarter_'+name+'.png'
        destination_path = wpath+'/'+ folders[i]+'/'+prefix[i]+wmname+'.png'
        copy(src_path, destination_path)
        '''
        if os.path.isfile(src_path):
            img = cv2.imread(src_path, cv2.IMREAD_UNCHANGED)
            img = cv2.resize(img, (505,505), interpolation= cv2.INTER_LINEAR)
            cv2.imwrite(destination_path, img)
            
        else:
            print("couldnt find "+ src_path)
        '''
def copyfiles(name, newname, wpath):
    #folders = ["aerialways","bridges","PowerReady","lakes","peaks","talwind"]
    #prefix = ["aerialway_","bridge_","cables_","lakes_","peaks_","talwind_"]
    #folders = ["rivers","roads, building"]
    #prefix = ["river_","rw_","b_"]
    folders = ["nmap_small_"]
    prefix = ["n_"]
    for i in range (len(folders)):
        src_path = name +'/'+folders[i]+name+'.png'
        destination_path = wpath+'/'+ folders[i]+'/'+prefix[i]+newname+'.png'
        if os.path.isfile(src_path):
            copy(src_path, destination_path)
        else:
            print("couldnt find "+ src_path)

names = []
newnames = []
jsonfiles = [""]
### iterate all tiles in tileselection 
#
with open(str(sector)+'.geojson', 'r') as file:
#with open('tileselection.geojson', 'r') as file:
    data = json.load(file)
    for f in data["features"]:
        n = f["properties"]["name"].split("|")
        names.append(str(n[0]).replace(" ",""))
        newnames.append(str(n[1]).replace(" ",""))

print(newnames)



c = 0
for n in names:
    #add = n.split("_")
    #postprocessHmap.closegaps((int(add[0]),int(add[1])))
    #print("{"+ str(add[0])+","+str(add[1])+"},")
    copyfilesForSectors(n, newnames[c], wpath)
    #copyWind(n,newnames[c],"w")

    c += 1
    '''
### create items if they dont exist
    path = n+"/hmap"+n+".png"
    #path = n+"/landscape.stl"
    if os.path.isdir(n):
        if os.path.isfile(path):
            #print("{"+ str(add[0])+","+str(add[1])+"},")

            print(n)
            c += 1
            #makeLakes.cropGeoJsonLineFeature(n)
            #
            
            try:
                alt = cv2.imread(path, cv2.IMREAD_UNCHANGED) #, cv2.IMREAD_GRAYSCALE
                cv2.imwrite(n+"/nmap_small_"+n+".png", normalfromhightmap.makeNormalmap(alt))
                
                #makeBuildingGeometry.makeBuildings(n)
                #makeLandscapeMesh.createMesh(n)
                #makeLakes.makeRoadMesh(n)
                #makeLakes.makeRiverMesh(n)
            except:
                print(n +" something went wrong")
           # makeLakes.makeLakes(n)
           

#print(str(c) +"x not found")
'''  