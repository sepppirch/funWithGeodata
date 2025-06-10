import numpy as np

def findLoopDir(polyRed):
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
        return polyRed

def pointInTriangle(P,A,B,C):
    # point P is inside Triangle ABC if all cross products are negative

    CA = np.subtract(A, C)
    AB = np.subtract(B, A)
    BC = np.subtract(C, B)

    AP = np.subtract(P, A)
    BP = np.subtract(P, B)
    CP = np.subtract(P, C)

    if np.cross(CA, AP) < 0 and np.cross(AB, BP) < 0 and np.cross(BC, CP) < 0:
        return True
    else:
        return False
    
def clipEars(verts):
    faces = []
    indexlist = []
    #populate Index list
    
    for i in range(len(verts)):
        indexlist.append(i)
    i = 0
    ii = 0
    while (len(indexlist) > 3) and (ii < 1000): # 
    #for z in range (20):
        ii +=1
        iA = indexlist[i]
        iB = indexlist[(i + 1) % len(indexlist)] 
        iC = indexlist[(i - 1) % len(indexlist)]
        ##print("testing index " + str(iC) + " " + str(iA) + " "+ str(iB))
        A = verts[iA]
        B = verts[iB]
        C = verts[iC]
        AB = np.subtract(B, A)
        AC = np.subtract(C, A)
        # Test Corner A ANGLE 
        
        if  np.cross(AC, AB) > 0:
            ##print("first test passed" + str(np.cross(AC, AB)))
            # check if any other point lies within triangle
            isINside = False
            for x in indexlist:
                # Dont test for A B C
                if (x != iA) and (x != iB) and (x != iC):
                    P = verts[x]
                    if pointInTriangle(P,A,B,C):
                        isINside = True
                        break
            if not isINside:
                # valid triangle
                newTri = [iB,iA,iC]
                faces.append(newTri)
                indexlist.remove(iA)
                ##print(indexlist)
                i = 0
                ##print("test passed, adding " + str(newTri))
            else:
                i = (i + 1) % len(indexlist)
                ##print("second test failed")
        else:
            ##print("first test failed")
            i = (i + 1) % len(indexlist)
    if ii == 1000:     
        print("triangulation failed")
        return False
    else:
        last = [indexlist[1],indexlist[0],indexlist[2]]
        faces.append(last)
        return faces