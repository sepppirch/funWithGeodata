
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
nsize = []
lsize = []

npos = []

nc = 8000
lc = 8000

ns = 0.5
ls = 0.5

for i in range (nc):

    voffset = i * len(Cverts)
    uoffset = i * len(CUVs)
    uv = [i%128, 127 -int(i/128)]
    grid = [i%64, 63 -int(i/64)]
    pos = [random.uniform(-100, 100),random.uniform(-100, 100),random.uniform(-100, 100)]
    p = np.array([float(grid[0])*2, float(grid[1])*2, 0.0])
    p1 = np.array([640,0,0])
    p2 = np.array([0,0,0])
    v = p1-p
    v2 = p2-p
    l2 = np.linalg.norm(v2)/10 + np.pi/2*3
    l = np.linalg.norm(v)/2
    nsize.append(random.uniform(0.5, 2))
    #pos = [float(grid[0])*2, float(grid[1])*2,  np.sin(l2)*3 ]
    npos.append(pos)
    for v in Cverts:
        #vr = np.dot(v,m)
        verts.append([v[0]* nsize[i] +pos[0],v[1]* nsize[i] +pos[1], v[2]* nsize[i] +pos[2]])
    for u in CUVs:
        UVs.append([u[0]+uv[0]/128, u[1]+uv[1]/128])
    for t in Ctriangles:
        triangles.append([t[0]+ voffset, t[1]+ voffset, t[2]+ voffset, t[3]+ voffset])
    for x in CtrianglesUV:
        trianglesUV.append([x[0]+ uoffset, x[1]+ uoffset, x[2]+ uoffset, x[3]+ uoffset])



#linklist = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [15, 16], [16, 17], [17, 18], [18, 19], [19, 20], [20, 21], [21, 22], [22, 23], [23, 24], [24, 25], [25, 26], [26, 27], [27, 28], [28, 29], [29, 30], [30, 31], [31, 32], [32, 33], [33, 34], [34, 35], [35, 36], [36, 37], [37, 38], [38, 39], [39, 40], [40, 41], [41, 42], [42, 43], [43, 44], [44, 45], [45, 46], [46, 47], [47, 48], [48, 49], [49, 50], [50, 51], [51, 52], [52, 53], [53, 54], [54, 55], [55, 56], [56, 57], [57, 58], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100]]
linklist = []

for i in range (lc):
    #
    '''
    if int(i/64) != 63:
        linklist.append([i,i+64])

    if i%64 != 63:
        linklist.append([i,i+1])
    '''
    l = [random.randrange(0,nc-1),random.randrange(0,nc-1)]
    linklist.append(l)

## links
#print(linklist)
#linklist = [[0,1],[0,2],[0,3]]
Lverts = []
LUVs = []
Ltriangles = []
LtrianglesUV = []

i = 0

nverts = len(verts)
nuv = len(UVs)
for l in linklist:
    scale = random.uniform(0.2, 0.6)
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
    #print(l)
    #print (np.dot(a,b))
    #k = np.array([ 0.59500984,  0.09655469, -0.79789754])
    x = np.random.randn(3)  # take a random vector
    x -= x.dot(k) * k / np.linalg.norm(k)**2      # make it orthogonal to k
    x /= np.linalg.norm(x)
    y = np.cross(k, x)
    m = np.array([k*l,x*scale,y*scale])
    #print(m)


    voffset = i * len(Cverts)
    uoffset = i * len(CUVs)
    uv = [i%512, 512 -int(i/512)]
    pos = p
     

    for v in Cverts:
        vr = np.dot(v,m)
        verts.append([vr[0]+pos[0],vr[1]+pos[1], vr[2]+pos[2]])
    for u in CUVs:
        UVs.append([u[0]/4+uv[0]/512, u[1]*2+uv[1]/64-7.015625] )
    for t in Ctriangles:
        Ltriangles.append([t[0]+ voffset + nverts, t[1]+ voffset + nverts, t[2]+ voffset + nverts, t[3]+ voffset + nverts])
    for x in CtrianglesUV:
        LtrianglesUV.append([x[0]+ uoffset + nuv, x[1]+ uoffset + nuv, x[2]+ uoffset + nuv, x[3]+ uoffset + nuv])
    i += 1


name = "Testrandom_"+str(nc)+"_"+str(lc)+".obj"
open(name, 'w').close()
with open(name, 'a') as f1:
    for v in verts:
        line = "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + '\n'
        f1.write(line)
    for u in UVs:
        line = "vt " + str(u[0]) + " " + str(u[1]) +'\n'
        f1.write(line)

    f1.write('\ng nodes4''\nusemtl nodes''\n')
    c = 0
    for t in triangles:
            line = "f " + str(t[0] +1) + "/" +str(trianglesUV[c][0] +1) + " "+ str(t[1] +1) + "/" +str(trianglesUV[c][1] +1) +" "+ str(t[2] +1) + "/"+ str(trianglesUV[c][2] +1)  +" "+ str(t[3] +1) + "/"+ str(trianglesUV[c][3] +1) + '\n'
            f1.write(line)
            c+=1


    f1.write('\ng links4''\nusemtl links''\n')
    c = 0
    for t in Ltriangles:
            line = "f " + str(t[0] +1) + "/" +str(LtrianglesUV[c][0] +1) + " "+ str(t[1] +1) + "/" +str(LtrianglesUV[c][1] +1) +" "+ str(t[2] +1) + "/"+ str(LtrianglesUV[c][2] +1)  +" "+ str(t[3] +1) + "/"+ str(LtrianglesUV[c][3] +1) + '\n'
            f1.write(line)
            c+=1


