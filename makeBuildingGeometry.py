import os
import json
import re
import cv2
from datetime import datetime
import math
from geotiff import GeoTiff
import numpy as np
import random 
import earclipping




def makeBuildings(name):
    vtest =[[0.40177516025493576, 0.9507715650102441], [0.4008814102549274, 0.9504795942073484], [0.4009314102549344, 0.9503153606307317], [0.40081891025492977, 0.9501693752292515], [0.40100016025492735, 0.9501055066161443], [0.40105641025492966, 0.9499139007766934], [0.4013314102549348, 0.9499960175650017], [0.40142516025493125, 0.9496675504117684], [0.4011439102549308, 0.9495854336233952], [0.4011939102549378, 0.9493938277840092], [0.40107516025493783, 0.9492295942073277], [0.40128766025493423, 0.9491748496817887], [0.4013376602549301, 0.9489923679299708], [0.40161266025493525, 0.9490744847182792], [0.4017126602549381, 0.9487186453022763], [0.4014064102549342, 0.9486365285139032], [0.4014626602549365, 0.9484540467620853], [0.40136891025492893, 0.9482989372730368], [0.4015189102549277, 0.9482350686599297], [0.4015689102549347, 0.9480434628204788], [0.4018689102549322, 0.9481347036964202], [0.40196266025492866, 0.9477971124555538], [0.40161266025493525, 0.9476967474920442], [0.4017001602549364, 0.9475233898277945], [0.4015689102549347, 0.9473409080759766], [0.40171891025493345, 0.9472679153752365], [0.40177516025493576, 0.9470580613606491], [0.40216891025492973, 0.9471675504117268], [0.4023689102549355, 0.9464558715795917], [0.4020001602549339, 0.9463463825285139], [0.4020564102549362, 0.9461547766891277], [0.401950160254938, 0.9459905431124462], [0.40212516025492917, 0.9459905431124462], [0.4021876602549379, 0.9457715650102907], [0.4030939102549369, 0.946036163550417]]
    #vtest = [[0,0],[0,1],[1,1],[0.9,0.5],[1,0]]
    vtest1 = np.divide(vtest,1)

    vtest2 = vtest1 + [0.02, 0.02]
    vtest0 = np.divide([[0,0],[0,1],[1,1],[1,0]],1000) + [0.01, 0.01]
    varray = []

    #varray.append(vtest1)
    #varray.append(vtest0)
    #varray.append(vtest2)
    #print(vtest1)
    vtest1 = vtest1[::-1]
    ##print(pointInTriangle([-0.1,0.6],[0,1],[1,0],[0.0]))
    ##print(clipEars(v))
    ##print(len(v))

    #name = "-1_-1"
    size = 204000
    hightest = -2000000
    hmap = cv2.imread(name +'/hmap_burnIn_'+name+'.png', cv2.IMREAD_UNCHANGED)

    ###print(hmap[0][0])

    f = open(name+'/buildings_reduced_'+name+'.json')
    data = json.load(f)


    #f1 = data["features"][0]
    verts = []

    trianglesWall = [[],[],[],[],[],[],[],[],[],[]]
    trianglesWindow = [[],[],[],[],[],[],[],[],[],[]]
    trianglesDoor = [[],[],[],[],[],[],[],[],[],[]]
    trianglesRoof = [[],[],[],[],[],[],[],[],[],[]]
    randMat = 0

    ##print(len(data["features"]))
    UVs = [[0.0,0.0],[0.0,1],[1,1],[1,0],[2,0.5]]

    for sample in range (len(data["features"])-1):#data["features"]:
    #for sample in range (1000):
    #if len(data["features"][x]["geometry"]["coordinates"]) > 0:
        lengthVerts = len(verts)
        lengthUV = len(UVs)
        poly = []
        polyRed = []
        workUVs=[]
        workverts = []
        ring2 =[]
        ring3 = []
        ring4 = []
        buildingHeight = 0
        circumference = 0        
        woodhouse = False
        #poly = varray[sample]   
        
        if "height" in data["features"][sample]["properties"]:
            try:
                buildingHeight = int(float(data["features"][sample]["properties"]["height"].replace("m", "").replace(",", ".")) / 3)*100
            except:
                buildingHeight = 0
            if buildingHeight > 2000:
                buildingHeight = 0
        for p in data["features"][sample]["geometry"]["coordinates"]:
            poly.append(p) 

        poly.pop()

        # Prepare Data
        
        for c in range(len(poly)):

            a = poly[(c-1) % len(poly)]
            b = poly[c]
            pc = poly[(c+1) % len(poly)]
            ba = np.subtract(a, b)
            bc = np.subtract(pc, b)
            iba = np.subtract(b, a)
            ibc = np.subtract(b, pc)
            angle1 = np.arctan2(bc[1], bc[0]) - np.arctan2(ba[1], ba[0])
            angle2 = np.arctan2(ibc[1], ibc[0]) - np.arctan2(iba[1], iba[0])
            seglength = np.linalg.norm(bc)
            seglength1 = np.linalg.norm(ba)
            circumference += seglength
            direction = np.cross(ba, bc)
            #print(seglength)

            Athresh = 15
            #print(np.rad2deg(angle2)%180)
            #if not abs(np.rad2deg(angle2)) < Athresh or abs(abs(np.rad2deg(angle2)) - 180) < Athresh:
            if seglength > 0.00004 :
                if not np.rad2deg(angle2) % 180 < Athresh :
                    if not (180 - (np.rad2deg(angle2)% 180)) < Athresh:
                            polyRed.append(poly[c])


        culmAngles = 0

        for c in range(len(polyRed)):

            a = polyRed[(c-1) % len(polyRed)]
            b = polyRed[c]
            pc = polyRed[(c+1) % len(polyRed)]
            ba = np.subtract(a, b)
            bc = np.subtract(pc, b)
            iba =  np.subtract(b, a)
            ibc =  np.subtract(pc, b)
            angle1 = np.arctan2(bc[1], bc[0]) - np.arctan2(ba[1], ba[0])
            angle2 = np.arctan2(ibc[1], ibc[0]) - np.arctan2(iba[1], iba[0])
            direction = np.cross(ba, bc)
            seglength = np.linalg.norm(bc)
            #print(seglength)
            ang = 0


            #print (np.rad2deg(angle1))
            angle3 = abs(np.rad2deg(angle2))
            if angle3 > 180:
                angle3 = 360 - angle3
            #print (angle3)

            if direction < 0:
                ang = angle3
            else:
                ang = angle3 * -1
            culmAngles += ang

        ##
        #print(culmAngles)
        # reverse Point Order
        if culmAngles > 0:
            polyRed = polyRed[::-1] #reverse order
            ##print("counter clockwise")
        #else:
            ##print("clockwise")
        #print(buildingHeight)
        if buildingHeight == 0:
            #print(circumference)
            buildingHeight = int(circumference*40000)+ 1 * 75
            
            if buildingHeight > 400:
                buildingHeight = random.randint(2,3) * 100
        #print(circumference)

        # Resort for Saddle ROOF
        if len(polyRed) == 4:
            AB = np.subtract(polyRed[0], polyRed[1])
            BC = np.subtract(polyRed[1], polyRed[2])

            if np.linalg.norm(AB) < np.linalg.norm(BC):
                ##print(polyRed)
                lastP =  polyRed[len(polyRed)-1]
                polyRed.insert(0,lastP)
                polyRed.pop()
                #print(polyRed)
            randMat = random.randint(1,5)
        else:
            randMat = random.randint(6,9)




        #p1 = np.array([data["features"][sample]["geometry"]["coordinates"][0][0] , data["features"][sample]["geometry"]["coordinates"][0][1]])
        if len(polyRed) > 3:
            p1 = polyRed[0]
            if p1[0] < 1 and p1[0] > 0 and p1[1] < 1 and p1[1] > 0 : 
                    
                #if p1[0] <= 1 and p1[0] >= 0 and p1[1] <= 1 and p1[1] >= 0 :

                    # get Z coordinate from hightmap
                    c = hmap[int(p1[1]*2041)][int(p1[0]*2041)]*1.5625 - 51200
                    #if c > hightest:
                    #    hightest = c
                    #if c < -26000:
                    #c = 0.0
                    for p in polyRed:
                        #x = [(p[0]-p1[0])*size , (p[1]-p1[1])*size , c]
                        x = [p[0]*size , p[1]*size , c]
                        workverts.append(x)
                    ringcount = len(polyRed)
                    ##print(count)
                    #resized.append(resized[0])
                    ring1 = workverts.copy()

                    for p in ring1:
                        xt = [p[0] , p[1] , p[2] + buildingHeight]
                        ring2.append(xt)
                        workverts.append(xt)



                    if ringcount > 4:
                        # MAKE VERTS FOR FLAT ROOF
                        bevel = 10
                        

                        # INLINE BEVEL
                        for i in range (len(ring2)):
                            a = ring2[(i-1) % len(ring2)]
                            b = ring2[i]
                            c = ring2[(i+1) % len(ring2)]
                            ab = np.subtract(a, b)
                            cb = np.subtract(c, b)
                            abNorm= ab / (np.linalg.norm(ab))
                            cbNorm= cb / (np.linalg.norm(cb))
                            #direction = np.cross([abNorm[0],abNorm[1]], [cbNorm[0],cbNorm[1]])
                            direction = np.cross(ab, cb)
                            p = [0,0,0]

                            if direction[2] > 0:
                                p = b + abNorm * bevel+ cbNorm * bevel
                                #p = np.sum(l, axis=0) 

                            else:
                                #l = [b, abNorm * bevel , cbNorm * bevel*-1]
                                p = b + abNorm * bevel* -1  + cbNorm * bevel* -1 
                    #            p = np.add(b,abNorm * bevel *-1)
                    #           p = np.add(b,cbNorm * bevel)
                            bp = np.subtract(p, b)
                            bpnorm = bp / np.linalg.norm(bp)
                            p1 = b + bpnorm * bevel
                            workverts.append(p1)
                            ring3.append(p1)


                        for p in (ring3):
                            tp = [p[0],p[1], p[2] - bevel]
                            tp1 = [p[0],p[1]]
                            workverts.append(tp) 
                            ring4.append(tp1)

                    elif ringcount == 4:
                        
                        A = ring2[0]
                        B = ring2[1]
                        C = ring2[2]
                        D = ring2[3]

                        AD = np.subtract(D, A)
                        BC = np.subtract(C, B)
                        AB = np.subtract(A, B)
                        
                        ABn = AB/ np.linalg.norm(AB) *30
                        if np.linalg.norm(AB) > 1000:
                            roofangle = 10
                        else:
                            roofangle = random.randint(2,4)
                        G1 = A + AD/2 + [0,0,np.linalg.norm(AD)/roofangle]
                        G2 = B + BC/2 + [0,0,np.linalg.norm(BC)/roofangle]
                        G3 = G1 + ABn
                        G4 = G2 - ABn
                        AG1 = np.subtract(A, G1)
                        DG1 = np.subtract(D, G1)
                        G5 = G3 + AG1*1.25
                        G7 = G3 + DG1*1.25
                        G6 = G4 + AG1*1.25
                        G8 = G4 + DG1*1.25

                        workverts.append(G1)
                        workverts.append(G2)
                        workverts.append(G3)
                        workverts.append(G4)
                        workverts.append(G5)
                        workverts.append(G6)
                        workverts.append(G7)
                        workverts.append(G8)
                    #else:
                        ##print("less then 4 points")
                        woodhouse = False

                    for i in range(ringcount):
                        # get length of segment for UVS
                        
                        rows = 2
                        #col = int(buildingHeight/100)
                        a = workverts[i]
                        b = workverts[(i+1)%ringcount]
                        ba = np.subtract(b, a)
                        lenAB= np.linalg.norm(ba)/100
                        if lenAB > 1:
                            rows = int(lenAB)
                        else: 
                            rows = 1
                        
                            
                        if random.randint(0,3)==0:
                            woodhouse = True
                        else:
                            woodhouse = False
                        #print(str(rows))
                    if woodhouse: 
                        randMat = 0

                    # MAKE TRIANGLES FOR WALLS
                    ringNum = 0
                    door = 0

                    for i in range(ringcount):
                        # get length of segment for UVS
                        
                        rows = 2
                        col = int(buildingHeight/100)
                        a = workverts[i]
                        b = workverts[(i+1)%ringcount]
                        ba = np.subtract(b, a)
                        lenAB= np.linalg.norm(ba)/100
                        if lenAB > 1:
                            rows = int(lenAB)
                        else: 
                            rows = lenAB

                        #print(str(col) + "---" + str(rows))

                        walluvs=[[0.0,0.0],[0.0,rows],[col,rows],[col,0]]

                        for u in walluvs:
                            workUVs.append(u)

                        uvt1 = [i*4+lengthUV, 1+i*4+lengthUV, 3+i*4+lengthUV]
                        #uvt1 = [0,0,0]
                        uvt2 = [2+i*4+lengthUV, 3+i*4+lengthUV, 1+ i*4+lengthUV]

                        t1 = [i + ringcount + ringNum*ringcount +lengthVerts, uvt1[2], (i+1)%ringcount + ringNum*ringcount+lengthVerts, uvt1[1], i + ringNum*ringcount +lengthVerts, uvt1[0]]
                        t2 = [(i+1)%ringcount+ ringNum*ringcount+lengthVerts, uvt2[2], i + ringcount + ringNum*ringcount+lengthVerts, uvt2[1], (i+1) % ringcount + ringcount + ringNum*ringcount+lengthVerts, uvt2[0]]

                        if rows < 1:
                            trianglesWall[randMat].append(t1)
                            trianglesWall[randMat].append(t2)
                        elif door == 0:
                            trianglesDoor[randMat].append(t1)
                            trianglesDoor[randMat].append(t2)
                            door = 1
                        else:
                            trianglesWindow[randMat].append(t1)
                            trianglesWindow[randMat].append(t2)




                    # MAKE TRIANGLES FOR FLAT ROOOF
                    if ringcount > 4:

                        ringNum = 1

                        uvt2 = [0,1,3]
                        uvt1 = [1,3,2]

                        for i in range(ringcount):

                            t1 = [i + ringcount + ringNum*ringcount +lengthVerts, uvt1[0], (i+1)%ringcount + ringNum*ringcount+lengthVerts, uvt1[1], i + ringNum*ringcount +lengthVerts, uvt1[2]]
                            t2 = [(i+1)%ringcount+ ringNum*ringcount+lengthVerts, uvt2[0], i + ringcount + ringNum*ringcount+lengthVerts, uvt2[1], (i+1) % ringcount + ringcount + ringNum*ringcount+lengthVerts, uvt2[2]]


                            trianglesWall[randMat].append(t1)
                            trianglesWall[randMat].append(t2)



                        ringNum = 2

                        for i in range(ringcount):
                            # get length of segment for UVS

                            t1 = [i + ringcount + ringNum*ringcount +lengthVerts, uvt1[0], (i+1)%ringcount + ringNum*ringcount+lengthVerts, uvt1[1], i + ringNum*ringcount +lengthVerts, uvt1[2]]
                            t2 = [(i+1)%ringcount+ ringNum*ringcount+lengthVerts, uvt2[0], i + ringcount + ringNum*ringcount+lengthVerts, uvt2[1], (i+1) % ringcount + ringcount + ringNum*ringcount+lengthVerts, uvt2[2]]

                            trianglesWall[randMat].append(t1)
                            trianglesWall[randMat].append(t2)

                        ringNum = 3



                        roof = earclipping.clipEars(ring4)
                        if roof == False:
                            print("triangulation failed!!!")
                            print(polyRed)
                        else:
                            for p in (ring4):
                                workUVs.append([p[0]/1000, p[1]/1000])
                            
                            for i in roof:
                                    
                                    #t = [i[0] + ringNum*ringcount + lengthVerts, 1, i[1]+ ringNum*ringcount +lengthVerts, 1, i[2] + + ringNum*ringcount+lengthVerts, 1]
                                    #thisUV = lengthUV + ringcount * 4 + i[0]  
                                    t = [i[0] + ringNum * ringcount + lengthVerts,  lengthUV + ringcount * 4 + i[0], i[1] + ringNum*ringcount +lengthVerts,  lengthUV + ringcount * 4 + i[1], i[2] + ringNum*ringcount+lengthVerts,  lengthUV + ringcount * 4 + i[2]] 
                                    trianglesRoof[randMat].append(t)        
                    
                    
                    
                    elif ringcount == 4:
                        '''
                        t1 = [9+ lengthVerts,0, 5+ lengthVerts,1, 4+ lengthVerts,2]
                        t2 = [4+ lengthVerts,2, 8+ lengthVerts,3, 9+ lengthVerts,0]

                        t3 = [8+ lengthVerts,0, 7+ lengthVerts,1, 6+ lengthVerts,2]
                        t4 = [6+ lengthVerts,2, 9+ lengthVerts,3, 8+ lengthVerts,0]
                        '''
                        t1 = [11+ lengthVerts,0, 13+ lengthVerts,1, 12+ lengthVerts,2]
                        t2 = [12+ lengthVerts,2, 10+ lengthVerts,3, 11+ lengthVerts,0]

                        t3 = [10+ lengthVerts,0, 14+ lengthVerts,1, 15+ lengthVerts,2]
                        t4 = [15+ lengthVerts,2, 11+ lengthVerts,3, 10+ lengthVerts,0]

                        #t5 = [9+ lengthVerts,4, 6+ lengthVerts,0, 6 + lengthVerts,1]
                        #t6 = [8+ lengthVerts,4, 4+ lengthVerts,0, 7 + lengthVerts,1]
                        
                        t5 = [5+ lengthVerts,0, 9+ lengthVerts,4, 6 + lengthVerts,1]
                        t6 = [7+ lengthVerts,1, 8+ lengthVerts,4, 4 + lengthVerts,0]

                        trianglesRoof[randMat].append(t1)
                        trianglesRoof[randMat].append(t2)

                        trianglesRoof[randMat].append(t3)
                        trianglesRoof[randMat].append(t4)

                        trianglesWall[randMat].append(t5)
                        trianglesWall[randMat].append(t6)

                    ##print(workUVs)
                    #inline BEVEL for flat roof
                    for i in range(ringcount):
                        n = i + ringcount
                        ##print(workverts[n])



                    for p in workverts:
                        verts.append(p)
                    for p in workUVs:
                        UVs.append(p)
            #else:
                    #print("p0 out of range") 
                    #print(polyRed)  
    print(hightest)
    open(name +'/building_s_'+name+'.obj', 'w').close()
    with open(name +'/building_s_'+name+'.obj', 'a') as f1:
        for v in verts:
            line = "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + '\n'
            f1.write(line)

        for u in UVs:
            line = "vt " + str(u[0]) + " " + str(u[1]) +'\n'
            f1.write(line)

        for i in range(len(trianglesWall)):
            f1.write('\ng wall'+str(i)+'\nusemtl wall'+str(i)+'\n')
            for t in trianglesWall[i]:
                line = "f " + str(t[0] +1) + "/" +str(t[1] +1) + " "+ str(t[2] +1) + "/" +str(t[3] +1) +" "+ str(t[4] +1) + "/"+ str(t[5] +1) + '\n'
                f1.write(line)
        for i in range(len(trianglesWindow)):
            f1.write('\ng Window'+str(i)+'\nusemtl Window'+str(i)+'\n')
            for t in trianglesWindow[i]:
                line = "f " + str(t[0] +1) + "/" +str(t[1] +1) + " "+ str(t[2] +1) + "/" +str(t[3] +1) +" "+ str(t[4] +1) + "/"+ str(t[5] +1) + '\n'
                f1.write(line)
        for i in range(len(trianglesDoor)):
            f1.write('\ng Door'+str(i)+'\nusemtl Door'+str(i)+'\n')
            for t in trianglesDoor[i]:
                line = "f " + str(t[0] +1) + "/" +str(t[1] +1) + " "+ str(t[2] +1) + "/" +str(t[3] +1) +" "+ str(t[4] +1) + "/"+ str(t[5] +1) + '\n'
                f1.write(line)
        for i in range(len(trianglesRoof)):
            f1.write('\ng Roof'+str(i)+'\nusemtl Roof'+str(i)+'\n')
            for t in trianglesRoof[i]:
                line = "f " + str(t[0] +1) + "/" +str(t[1] +1) + " "+ str(t[2] +1) + "/" +str(t[3] +1) +" "+ str(t[4] +1) + "/"+ str(t[5] +1) + '\n'
                f1.write(line)

from area import area




def filterBuildings(name):
    f = open(name+'/buildings_'+name+'.json')
    data = json.load(f)
    dataF = {"features":[]}

    print(len(data["features"]))
    
    

    for sample in data["features"]:
        sample["area"] = Area(sample["geometry"]["coordinates"])
        if sample["area"] > 10:
            dataF["features"].append(sample)
         
    dataF["features"].sort(key = lambda json: json['area'], reverse=True)
    #print(dataF)
    if len(dataF["features"])>4000:
        dataF["features"]=dataF["features"][0:4000]

    with open(name +'/buildings_reduced_'+name+'.json', 'w') as f:
        json.dump(dataF, f)



def Area(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    #print (area*10000000)
    return area*10000000

#filterBuildings("2_-4")
#makeBuildings("2_-4")