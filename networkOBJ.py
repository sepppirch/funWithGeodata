
import random
import numpy as np

Cverts =[[-0.5, -0.5, -0.5],[-0.5, 0.5, -0.5],[0.5, 0.5, -0.5],[0.5, -0.5, -0.5],[-0.5, -0.5, 0.5],[0.5, -0.5, 0.5],[0.5, 0.5, 0.5],[-0.5, 0.5, 0.5]]
CUVs=[[0,0],[0.0078125,0],[0.0078125,0.0078125],[0,0.0078125]]
Ctriangles=[[0,1,2,3],[4,5,6,7],[0,3,5,4],[3,2,6,5],[2,1,7,6],[1,0,4,7]]
CtrianglesUV=[[0,1,2,3],[3,0,1,2],[3,0,1,2],[3,0,1,2],[3,0,1,2],[3,0,1,2]]

verts = []
UVs = []
triangles = []
trianglesUV = []

npos = []


for i in range (6):

    voffset = i * len(Cverts)
    uoffset = i * len(CUVs)
    uv = [i%128, 127 -int(i/128)]
    pos = [random.uniform(-100, 100),random.uniform(-100, 100),random.uniform(-100, 100)]
    npos.append(pos)
    for v in Cverts:
        #vr = np.dot(v,m)
        verts.append([v[0]+pos[0],v[1]+pos[1], v[2]+pos[2]])
    for u in CUVs:
        UVs.append([u[0]+uv[0]/128, u[1]+uv[1]/128])
    for t in Ctriangles:
        triangles.append([t[0]+ voffset, t[1]+ voffset, t[2]+ voffset, t[3]+ voffset])
    for x in CtrianglesUV:
        trianglesUV.append([x[0]+ uoffset, x[1]+ uoffset, x[2]+ uoffset, x[3]+ uoffset])

open('test1.obj', 'w').close()
with open('test1.obj', 'a') as f1:
    for v in verts:
        line = "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + '\n'
        f1.write(line)
    for u in UVs:
        line = "vt " + str(u[0]) + " " + str(u[1]) +'\n'
        f1.write(line)

    f1.write('\ng nodes''\nusemtl nodes''\n')
    c = 0
    for t in triangles:
            line = "f " + str(t[0] +1) + "/" +str(trianglesUV[c][0] +1) + " "+ str(t[1] +1) + "/" +str(trianglesUV[c][1] +1) +" "+ str(t[2] +1) + "/"+ str(trianglesUV[c][2] +1)  +" "+ str(t[3] +1) + "/"+ str(trianglesUV[c][3] +1) + '\n'
            f1.write(line)
            c+=1


## links
linklist = [[0,1],[0,2],[0,3]]
Lverts = []
LUVs = []
Ltriangles = []
LtrianglesUV = []

i = 0
for l in linklist:

    #a = np.random.randn(3)
    #b = np.random.randn(3)
    a = np.array(npos[l[0]])
    b = np.array(npos[l[1]])
    #b = np.array([[0.0, 1.0, 0.0],[1.0, 0.0, 0.0],[0.0, 0.0, 1.0]])
    c = a - b
    p = b + c/2

    k = c/np.linalg.norm(c)
    l = np.linalg.norm(c)
    #y = np.cross(c, [0,0,1])
    print(l)
    #print (np.dot(a,b))
    #k = np.array([ 0.59500984,  0.09655469, -0.79789754])
    x = np.random.randn(3)  # take a random vector
    x -= x.dot(k) * k / np.linalg.norm(k)**2      # make it orthogonal to k
    x /= np.linalg.norm(x)
    y = np.cross(k, x)
    m = np.array([k*l,x/5,y/5])
    print(m)


    voffset = i * len(Cverts)
    uoffset = i * len(CUVs)
    uv = [i%128, 127 -int(i/128)]
    pos = p
     

    for v in Cverts:
        vr = np.dot(v,m)
        Lverts.append([vr[0]+pos[0],vr[1]+pos[1], vr[2]+pos[2]])
    for u in CUVs:
        LUVs.append([u[0]+uv[0]/128, u[1]+uv[1]/128])
    for t in Ctriangles:
        Ltriangles.append([t[0]+ voffset, t[1]+ voffset, t[2]+ voffset, t[3]+ voffset])
    for x in CtrianglesUV:
        LtrianglesUV.append([x[0]+ uoffset, x[1]+ uoffset, x[2]+ uoffset, x[3]+ uoffset])
    i += 1

open('testLinks.obj', 'w').close()
with open('testLinks.obj', 'a') as f1:
    for v in Lverts:
        line = "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + '\n'
        f1.write(line)
    for u in LUVs:
        line = "vt " + str(u[0]) + " " + str(u[1]) +'\n'
        f1.write(line)
    f1.write('\ng nodes''\nusemtl nodes''\n')
    c = 0
    for t in Ltriangles:
            line = "f " + str(t[0] +1) + "/" +str(LtrianglesUV[c][0] +1) + " "+ str(t[1] +1) + "/" +str(LtrianglesUV[c][1] +1) +" "+ str(t[2] +1) + "/"+ str(LtrianglesUV[c][2] +1)  +" "+ str(t[3] +1) + "/"+ str(LtrianglesUV[c][3] +1) + '\n'
            f1.write(line)
            c+=1


