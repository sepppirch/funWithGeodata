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
    print(control_dist)
    # Add penalty if the distance between P1 and P2 exceeds max_control_dist
    penalty = 0
    if control_dist > max_control_dist:
        penalty = penalty_strength * (control_dist - max_control_dist)**2  # stronger quadratic penalty

    # Compute the Bézier curve error (least squares)
    t_vals = np.linspace(0, 1, len(points))
    curve = np.array([bezier_curve(t, P0, P1, P2, P3) for t in t_vals])
    curve_error = np.sum(np.linalg.norm(curve - points, axis=1) ** 2)

    return curve_error + penalty  # Total error with penalty

# Fit a single Bézier curve to the points
def fit_single_bezier_curve(points, max_control_dist=0.001, penalty_strength=10.0):
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

    
    plt.plot(curve[:, 0], curve[:, 1], "b-", label="Bézier curve")

    
    # Control points and the control polygon
    control_x = [P0[0], P1[0], P2[0], P3[0]]
    control_y = [P0[1], P1[1], P2[1], P3[1]]
    plt.plot(control_x, control_y, 'k--', alpha=0.5, label="Control polygon")




# Example usage with a single Bézier curve



name = "0_-1"
import json
# 10 random points (you can replace this with your own points)
f = open(name+'/trains_'+name+'.json')
data = json.load(f)
i = 2
points = np.array([[e[0], e[1]] for e in  data["coordinates"]]) 
print(len(points))
newpoints = np.array([])
# Fit Bézier spline to the 2D points (5 segments in this example)
num_segments = int(len(points)/20)


dist = 0



plt.figure(figsize=(8, 6))
plt.plot(points[:, 0], points[:, 1], "ro", label="Input points")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.title("Single Segment Bézier Curve")
plt.axis("equal")
# Fit the Bézier curve to the points
for i in range(10):
    if dist < 0.01:
        np.append(newpoints, np.array(points[i]), axis=0)
    else:
        break

segs = 8

for i in range(int(len(points)/segs) +1):

    s = i*segs
    e = i*segs+segs+1
    if e > len(points)-1:
        e = len(points)-1

    P0, P1, P2, P3 = fit_single_bezier_curve(points[s:e])
    # Plot the result
    plot_bezier_curve(points, P0, P1, P2, P3)




plt.show()

