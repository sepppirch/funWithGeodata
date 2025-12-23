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
def bezier_fit_error(params, points, max_control_dist=2.0, penalty_strength=1.0):
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
def fit_single_bezier_curve(points, max_control_dist=0.001, penalty_strength=1.0):
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
def plot_bezier_curve(points, P0, P1, P2, P3):
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
print(len(points))
newpoints = []
# Fit Bézier spline to the 2D points (5 segments in this example)
num_segments = int(len(points)/20)






plt.figure(figsize=(8, 6))
plt.plot(points[:, 0], points[:, 1], "ro", label="Input points")
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
    print(angle_deg)
    return angle_deg



groupedPoints = []
thisseg = []
dist = 0
thisdist = 0

maxd = 1
maxlen = 0.03
lastdir = 0.1
turn = 0
c = 0

for i in range(len(points)-2):
    
    p0 = np.array(points[i])
    p1 = np.array(points[i+1])
    p2 = np.array(points[i+2])
    
    thisdist = np.linalg.norm(points[i] - points[i+1])
    dist = dist + thisdist
    A = p1 - p0
    B = p2 - p1
    dir = findDirection(A,B)
    turn = turn+abs(dir)
    thisseg.append([points[i][0],points[i][1]])

   
    if  turn > 30  or thisdist * dir/5 > maxd :#and len(thisseg)>2:#or thisdist > maxd:
        lastdir = dir
        #
        
        #if len(thisseg)>1:
        thisseg.append([points[i+1][0],points[i+1][1]])
            #groupedPoints.append(thisseg)
        #else:
            #x = [ [thisseg[0][0],thisseg[0][1]], [ (thisseg[0][0] + thisseg[len(thisseg)-1][0])/2 ,(thisseg[0][1] + thisseg[len(thisseg)-1][1])/2],  [ (thisseg[0][0] + thisseg[len(thisseg)-1][0])/2 ,(thisseg[0][1] + thisseg[len(thisseg)-1][1])/2],  [thisseg[len(thisseg)-1][0],thisseg[len(thisseg)-1][1]]  ]
            
            #print("reee")
        #if len(thisseg)>3:
        groupedPoints.append(thisseg)

        c = c + 1
        thisseg = []
        turn = 0
        dist = 0

    '''
    thisdist = np.linalg.norm(points[i] - points[i+1])
    dist = dist + thisdist
        
    if  thisdist < maxd:
        thisseg.append([points[i][0],points[i][1]])
    else:
        if len(thisseg) < 3:
            
            thisseg = [points[i],points[i],points[i+1],points[i+1]]
        groupedPoints.append(thisseg)
        #
    
             
        if thisdist < 0.015:
            
            thisseg.append([points[i+1][0],points[i+1][1]])
        if len(thisseg)>2:
               
        if len(thisseg) > 2:
            groupedPoints.append([points[i],points[i],points[i+1],points[i+1]])
        
        #thisseg.append([points[i][0],points[i][1]])
        #dist = 0

        
        #i = i-1
        #thisseg.append([points[i][0],points[i][1]])
        #break
    '''
print(len(groupedPoints))
for seg in groupedPoints:
    



    newp = np.array(seg)




    P0, P1, P2, P3 = fit_single_bezier_curve(newp)
        # Plot the result
    plot_bezier_curve(points, P0, P1, P2, P3)




plt.show()

