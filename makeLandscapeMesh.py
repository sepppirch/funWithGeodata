import cv2
import json
import numpy as np

def createMesh(name):

    sidelen = 200
    verts = []
    tris = []
    offset = sidelen* sidelen
    highest = -51200
    lowest = 51200
    #name = "5_-29"
    size = 204200
    hightps = 200
    hmap = cv2.imread(name +'/hmap'+name+'.png', cv2.IMREAD_UNCHANGED)

    for x in range(sidelen):
        for y in range(sidelen):
            
            p1 = [x/(sidelen+1), y/(sidelen+1)]
            c = hmap[int(p1[0]*2041)][int(p1[1]*2041)] * 1.5625 - 51200
            verts.append([p1[0]* size, p1[1]*size , c])
            if c > highest:
                highest = c
            if c < lowest:
                lowest = c
            
    for x in range(sidelen):
        for y in range(sidelen):
            p1 = [x/(sidelen+1), y/(sidelen+1)]
            verts.append([p1[0]* size, p1[1]* size , -51200])


    #upper surface
    for x in range(sidelen - 1):
        for y in range(sidelen - 1):
            
            tri1 = [x + (y)*sidelen, x + (y+1)*sidelen, x + (y+1)*sidelen + 1]
            tri2 = [x + (y+1)*sidelen + 1, x + (y)*sidelen + 1, x + (y)*sidelen]
            tris.append(tri1)
            tris.append(tri2)
    #lower surface 
            
            tri1 = [  x + (y+1)*sidelen + 1 + offset, x + (y+1)*sidelen + offset, x + (y)*sidelen + offset]
            tri2 = [ x + (y)*sidelen+ offset,  x + (y)*sidelen + 1+ offset, x + (y+1)*sidelen + 1+ offset]
            tris.append(tri1)
            tris.append(tri2)

    #for x in range(sidelen - 1):

        tri1 = [x  + offset, x, x + 1]
        tri2 = [x + 1, x + 1 + offset, x + offset]
        tris.append(tri1)
        tris.append(tri2)

        tri1 = [x + (sidelen - 1)*sidelen + 1, x + (sidelen - 1)*sidelen, x + (sidelen - 1)*sidelen + offset]
        tri2 = [ x + (sidelen - 1)*sidelen + offset,  x + (sidelen - 1)* sidelen + offset + 1,  x + (sidelen - 1)*sidelen +1]
        tris.append(tri1)
        tris.append(tri2)

        tri1 = [(x + 1) * sidelen + offset, (x + 1) * sidelen, x * sidelen]
        tri2 = [x * sidelen, x * sidelen + offset, (x + 1) * sidelen + offset]
        tris.append(tri1)
        tris.append(tri2)

        tri1 = [x * sidelen + sidelen - 1,  (x + 1) * sidelen + sidelen - 1, (x + 1) * sidelen + offset + sidelen - 1]
        tri2 = [(x + 1) * sidelen + offset + sidelen - 1, x * sidelen + offset + sidelen - 1, x * sidelen + sidelen - 1]
        tris.append(tri1)
        tris.append(tri2)


    open(name +'/hmap'+name+ 'landscape.obj', 'w').close()
    with open(name +'/hmap'+name+ 'landscape.obj', 'a') as f1:
        for v in verts:
            line = "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + '\n'
            f1.write(line)


        for t in tris:
            line = "f " + str(t[0] +1) + " "+ str(t[1]+1)  +" "+ str(t[2]+1)  + '\n'
            f1.write(line)

    import meshio

    mesh = meshio.read(name +'/hmap'+name+ 'landscape.obj')
    meshio.write(name +'/landscape.stl', mesh, binary=True)

    out = {}
    out["lowest"] = lowest
    out["highest"] = highest

    json_object = json.dumps(out, indent=4)
    with open(name +"/params_"+name+".json",mode="w") as f:

        f.write(json_object)
