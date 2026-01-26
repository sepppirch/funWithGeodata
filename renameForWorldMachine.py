
import shutil 
from shutil import copy
import json

names = []
folders = ["forest","grass","hmaps","rocks"]
prefix = ["f_","g_","h_","r_"]

with open('F_quarter.geojson', 'r') as file:
    data = json.load(file)
    for f in data["features"]:
        n = f["properties"]["name"].split("|")
        names.append(n[0].replace(" ",""))
        #print(n[0])

#print(names)
#print("------------------")
bottomLeft = [16  ,-31]
w = 18
h = 18
for x in range (18):
    for y in  range(18):
        #bigtile = (y-1,x-13)



        wpath = "worldmachine_F/2041/"
        bigtile = (bottomLeft[1] + y + 18, bottomLeft[0] - x )
        
        name = str(bigtile[1])+"_"+str(bigtile[0])
        
        if name in names:
            print(name)

            
            newname = "_X"+ str(y) +"_Y" + str(x)
            src_path = name +'/hmap_burnIn_'+name+'.png'
            destination_path = wpath +'/hmaps/h'+newname+'.png'
            copy(src_path, destination_path)

            src_path = name +'/forestn'+name+'.png'
            destination_path = wpath+'/forest/f'+newname+'.png'
            copy(src_path, destination_path)

            src_path = name +'/icen'+name+'.png'
            destination_path = wpath+'/ice/i'+newname+'.png'
            copy(src_path, destination_path)

            src_path = name +'/grassn'+name+'.png'
            destination_path = wpath+'/grass/g'+newname+'.png'
            copy(src_path, destination_path)
        '''
        src_path = name +'/aerialways_'+name+'.json'
        destination_path = 'worldmachine/aerialways/aerialway_'+newname+'.json'
        copy(src_path, destination_path)

        src_path = name +'/building_'+name+'.obj'
        destination_path = 'worldmachine/buildings/b'+newname+'.obj'
        copy(src_path, destination_path)        

        src_path = name +'/swind'
        destination_path = 'worldmachine/swind/swind_' + newname
        shutil.copytree(src_path, destination_path)


        src_path = name +'/nmap_small_'+name+'.png'
        destination_path = 'worldmachine/nmaps/n'+newname+'.png'
        copy(src_path, destination_path)

 



        src_path = name +'/roads_'+name+'.obj'
        destination_path = 'worldmachine/roads/rw'+newname+'.obj'
        copy(src_path, destination_path)

        src_path = name +'/Bridges_'+name+'.json'
        destination_path = 'worldmachine/bridges/bridge'+newname+'.json'
        copy(src_path, destination_path)
        '''               

        '''



       

        

        
        src_path = name +'/roadsmask'+name+'.png'
        destination_path = 'worldmachine/roadsmask/rm'+newname+'.png'
        copy(src_path, destination_path)





        src_path = name +'/buildingHigh_'+name+'.obj'
        destination_path = 'worldmachine/buildings/bL'+newname+'.obj'
        copy(src_path, destination_path)

        src_path = name +'/nmap'+name+'.png'
        destination_path = 'worldmachine/nmap/n'+newname+'.png'
        copy(src_path, destination_path)
        
        

        src_path = name +'/sat'+name+'.jpg'
        destination_path = 'worldmachine/sat/s'+newname+'.jpg'
        copy(src_path, destination_path)
        



  

        


        src_path = name +'/lakes_'+name+'.json'
        destination_path = 'lakes/lakes'+newname+'.json'
        copy(src_path, destination_path)

        src_path = name +'/rivers_'+name+'.json'
        destination_path = 'rivers/rivers'+newname+'.json'
        copy(src_path, destination_path)

        src_path = name +'/roads_'+name+'.json'
        destination_path = 'roads/roads'+newname+'.json'
        copy(src_path, destination_path)

        
        src_path = name +'/lakesReady_'+name+'.json'
        destination_path = 'worldmachine/lakes/lakes'+newname+'.json'
        copy(src_path, destination_path)





        src_path = name +'/peaks_'+name+'.json'
        destination_path = 'worldmachine/peaks/peaks'+newname+'.json'
        copy(src_path, destination_path)
        
        src_path = name +'/PowerReady_'+name+'.json'
        destination_path = 'worldmachine/cables/cables'+newname+'.json'
        try:
                shutil.copy(src_path, destination_path)
        except:
             print("error")
        


        shutil.copytree(src_path, destination_path, dirs_exist_ok=True)  # Fine
    
        src_path = name +'/talwind_'+name+'.json'
        destination_path = 'worldmachine/talwind/talwind'+newname+'.json'
        copy(src_path, destination_path)    '''