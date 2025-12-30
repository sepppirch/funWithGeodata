import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Helper function: Cubic Bézier curve in 2D
def bezier_curve(t, P0, P1, P2, P3):
    return ((1 - t)**3 * P0 +
            3 * (1 - t)**2 * t * P1 +
            3 * (1 - t) * t**2 * P2 +
            t**3 * P3)

# Helper function: Compute error between Bézier curve and data points
def bezier_fit_error(params, points, max_control_dist, penalty_strength):
    P0 = params[0:2]
    P1 = params[2:4]
    P2 = params[4:6]
    P3 = params[6:8]
    
    # Compute distance between P1 and P2
    control_dist = np.linalg.norm(P1 - P2)
    #print(control_dist)
    # Add penalty if the distance between P1 and P2 exceeds max_control_dist
    penalty = 0
    if control_dist > max_control_dist:
        penalty = penalty_strength * (control_dist - max_control_dist)**2  # stronger quadratic penalty

    # Compute the Bézier curve error (least squares)
    t_vals = np.linspace(0, 1, len(points))
    curve = np.array([bezier_curve(t, P0, P1, P2, P3) for t in t_vals])
    curve_error = np.sum(np.linalg.norm(curve - points, axis=1) ** 2)
    #print(curve_error)
    return curve_error + penalty  # Total error with penalty

# Fit a single Bézier curve to the points
def fit_single_bezier_curve(points, max_control_dist=0.01, penalty_strength=2.0):
    # Initial guess for control points (start, middle, and end)
    P0 = points[0]  # Start point
    P3 = points[-1]  # End point
    P1 = points[len(points)//3]  # Approximate control point 1
    P2 = points[2*len(points)//3]  # Approximate control point 2

    # Optimize the control points
    init = np.hstack([P0, P1, P2, P3])
    result = minimize(bezier_fit_error, init, args=(points, max_control_dist, penalty_strength), method="Nelder-Mead")

    # Extract the optimized control points
    P1, P2 =  result.x[2:4], result.x[4:6]
    #P2 =  result.x[4:6]
    #P1, P2, P3 =  result.x[2:4], result.x[4:6], result.x[6:8]
    return P0, P1, P2, P3

# Plot the Bézier curve and the points
def plot_bezier_curve(P0, P1, P2, P3):
    t = np.linspace(0, 1, 300)
    curve = np.array([bezier_curve(ti, P0, P1, P2, P3) for ti in t])

    col = (np.random.random(), np.random.random(), np.random.random())
    plt.plot(curve[:, 0], curve[:, 1], "b-", label="Bézier curve", c=col)

    
    # Control points and the control polygon
    control_x = [P0[0], P1[0], P2[0], P3[0]]
    control_y = [P0[1], P1[1], P2[1], P3[1]]
    
    #plt.plot(control_x, control_y, 'k--', alpha=0.5, label="Control polygon")




# Example usage with a single Bézier curve



name = "0_-1"
import json
# 10 random points (you can replace this with your own points)
f = open(name+'/trains_'+name+'.json')
data = json.load(f)
i = 2
points = np.array([[e[0], e[1]] for e in  data["coordinates"]])
pointsC =  np.array([e[2] for e in  data["coordinates"]])
#print(len(points))
newpoints = []
# Fit Bézier spline to the 2D points (5 segments in this example)
#num_segments = int(len(points)/20)






plt.figure(figsize=(8, 6))
#print(points)
#plt.plot(points[:, 0], points[:, 1], "ro", markersize=2, label="Input points")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.title("Single Segment Bézier Curve")
plt.axis("equal")
# Fit the Bézier curve to the points



def findDirection(v1,v2):



    # 2D Cross Product (scalar for 2D)
    cross_prod = v1[0] * v2[1] - v1[1] * v2[0] # v1_x*v2_y - v1_y*v2_x

    # Dot Product
    dot_prod = np.dot(v1, v2)

    # Use arctan2(y, x) to get signed angle in radians (-pi to pi)
    angle_rad = np.arctan2(cross_prod, dot_prod)

    # Convert to degrees
    angle_deg = np.degrees(angle_rad)
    #print(angle_deg)
    return angle_deg



groupedPoints = []

subdPoints = []
thisseg = []
dist = 0
thisdist = 0

maxd = 2
maxlen = 0.01
lastdir = 0.1
turn = 0
c = 0

# find mean distance
distances = []
for i in range(len(points)-2):
    
    p0 = np.array(points[i])
    p1 = np.array(points[i+1])
    #p2 = np.array(points[i+2])
    
    thisdist = np.linalg.norm(points[i] - points[i+1])
    distances.append(thisdist)

mean_value = np.mean(distances)

print(mean_value)

newPoints = []

for i in range(len(points)):
    newPoints.append([points[i][0], points[i][1], pointsC[i]])
    #print(distances[i]/mean_value)
    if i < len(points)-2:
        iter = distances[i]/mean_value/2

        p0 = np.array([points[i][0], points[i][1], pointsC[i]])
        p1 = np.array([points[i+1][0], points[i+1][1], pointsC[i+1]])
        v = (p1 - p0)/iter
        if (int(iter)) > 1:
            for i in range(int(iter)):
                p = p0 + v*(i+1)
                newPoints.append([p[0], p[1], p[2]])
    #else:


plotpoints = np.array([[e[0], e[1]] for e in  newPoints])
plt.plot(plotpoints[:, 0], plotpoints[:, 1], "ro", markersize=2, label="Input points")
#plt.show()
'''
for i in range(len(points)-2):
    #thisseg.append([points[i][0], points[i][1], pointsC[i]])
    thisseg.append([points[i][0], points[i][1], pointsC[i]])


    if distances[i] > mean_value*6 :
        

        
        
        #thisseg.append([points[i][0], points[i][1], pointsC[i]])
        groupedPoints.append(thisseg)
        thisseg = []
        #i = i-1
        #if distances[i] > mean_value*2 :
        #print("reee")
        nextseg = []
        #nextseg.append([0.0, 0.0, 0.0])
        nextseg.append([points[i][0], points[i][1], pointsC[i]])
        nextseg.append([points[i+1][0], points[i+1][1], pointsC[i+1]])
        groupedPoints.append(nextseg)
        #print(thisseg)
        thisseg = []
        #else:
        #thisseg.append([points[i][0], points[i][1], pointsC[i]])
        
    #else:    


    #if i == len(points)-3:
        #thisseg.append([points[i+2][0],points[i+2][1], pointsC[i+2]])
groupedPoints.append(thisseg)

for p in groupedPoints:
    col = (np.random.random(), np.random.random(), np.random.random())
    for i in range(len(p)-1):
        p0 = [p[i][0], p[i+1][0]]
        p1 = [p[i][1], p[i+1][1]]
        #print(p0)
        #plt.plot([s[i][0],s[i][1]], [s[i+1][0],s[i+1][1]], marker = 'o')
        #plt.plot(p0, p1,  c=col)
       

finalPoints = []

for i, s in enumerate(groupedPoints):


    if len(s) == 1:
        print(len(s))
    elif len(s) == 2:
        #m1 = [(s[0][0]+s[1][0]) /2, (s[0][1]+s[1][1]) /2, s[0][2]]
        #m2 = [(s[0][0]+s[1][0]) /2, (s[0][1]+s[1][1]) /2, s[1][2]]
        x = [s[0],s[0],s[1],s[1]]
        #groupedPoints[i] = x
        finalPoints.append(x)
        #plot_bezier_curve(np.array(s[0]), np.array(s[1]), np.array(s[2]), np.array(s[3]))
    

    elif len(s) ==3:
        x = [s[0],s[1],s[1],s[2]]
        #groupedPoints[i] = x
        finalPoints.append(x)
        #plot_bezier_curve(np.array(s[0]), np.array(s[1]), np.array(s[2]), np.array(s[3]))
    #elif len(s) == 4:
        #x = [s[0],s[1],s[2],s[3]]
        #finalPoints.append(x)
    elif len(s) > 3:
        turn = 0
        splitseg = []
        #finalPoints.append(s)
''' 
s = newPoints 
finalPoints = []
splitseg = [] 
d = 0



for i in range(len(s)):
    splitseg.append(s[i])
    if i < len(s)-2:
        p0 = np.array([s[i][0],s[i][1]])
        p1 = np.array([s[i+1][0],s[i+1][1]])
        p2 = np.array([s[i+2][0],s[i+2][1]])
        thisdist = np.linalg.norm(p0 - p1)
        d = d + thisdist
        
        A = p1 - p0
        B = p2 - p1
        dir = findDirection(A,B)
        #print(dir)
        turn = turn + abs(dir)
        if i == len(s)-2:
            #print("finish")
            #splitseg.append(s[len(s)-2])
            #splitseg.append(s[len(s)-1])
            finalPoints.append(splitseg)
            turn = 0
            splitseg = []
            #print(d)
        elif  turn > 30 or d > 0.02: #count %13 == 0 or
            finalPoints.append(splitseg)
            turn = 0
            d = 0
            splitseg = []
            splitseg.append(s[i])


finalPoints.append(splitseg)    
             

'''

for i, s in enumerate(finalPoints):


    if len(s) == 1:
        print(len(s))
    elif len(s) == 2:
        #m1 = [(s[0][0]+s[1][0]) /2, (s[0][1]+s[1][1]) /2, s[0][2]]
        #m2 = [(s[0][0]+s[1][0]) /2, (s[0][1]+s[1][1]) /2, s[1][2]]
        x = [s[0],s[0],s[1],s[1]]
        finalPoints[i] = x
    elif len(s) ==3:
        x = [s[0],s[1],s[1],s[2]]
        #groupedPoints[i] = x
        finalPoints[i] = x
        #plot_bezier_curve(np.array(s[0]), np.array(s[1]), np.array(s[2]), np.array(s[3]))
    elif len(s) == 4:
        x = [s[0],s[1],s[2],s[3]]
        finalPoints[i] = x

'''

features = []
#Tin = []
#Tout = [[float(finalPoints[0][0][0]), float(finalPoints[0][0][1]),  float(finalPoints[0][0][2])]]

for s in finalPoints:
        '''
        if len(s)== 4:
            plot_bezier_curve(np.array(s[0]), np.array(s[1]), np.array(s[2]),np.array( s[3]))
            features.append([float(s[0][0]), float(s[0][1]), float(s[0][2])])   
            features.append([float(s[1][0]), float(s[1][1]), float(s[0][2])])
            features.append([float(s[2][0]), float(s[2][1]), float(s[len(s)-1][2])])
        else:
        '''
            #print(len(s))

            
        newp = np.array(s)
        newp = np.delete(newp,(2), axis=1)
        dist = np.linalg.norm(np.array([s[0][0],s[0][1]]) - np.array([s[len(s)-1][0],s[len(s)-1][1]]))
        print(dist)   
        P0, P1, P2, P3 = fit_single_bezier_curve(newp, dist/15)

        #check tangent lengths
        
        dist = np.linalg.norm(P0 - P3)
        distC1 = np.linalg.norm(P0 - P1)
        distC2 = np.linalg.norm(P2 - P3)

        if distC1 > dist/1.5:
            print("c1 too long")
            P1 = P0 + (P1 - P0)/distC1*dist/1.5
        if distC2 > dist/2:
            print("c2 too long")
            P2 = P3 + (P2 - P3)/distC2*dist/1.5
        
        features.append([float(P0[0]), float(P0[1]), float(s[0][2])])
        features.append([float(P1[0]), float(P1[1]), float(s[0][2])])
        features.append([float(P2[0]), float(P2[1]), float(s[len(s)-1][2])])
        
                # Plot the result
        plot_bezier_curve(P0, P1, P2, P3)
            #print(P0)
        
#print(finalPoints)
thisbezier =json.dumps({"points":[{"coordinates":features}]})
#print(Tin)

with open("F:/CLOUDBASE_git/Content/data/json/splines/bezier_X30_Y16.json", "w") as outfile:
    outfile.write(thisbezier)

#newp = np.array(Tin + Tout)
#print(len(Tout))
#plt.plot(newp[:, 0], newp[:, 1], "o", color="blue", markersize=4, label="Input points")
plt.show()

