import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Helper function: Cubic Bézier curve in 2D
def bezier_curve(t, P0, P1, P2, P3):
    return ((1 - t)**3 * P0 +
            3 * (1 - t)**2 * t * P1 +
            3 * (1 - t) * t**2 * P2 +
            t**3 * P3)

# Helper function: Fit cubic Bézier curve to a 2D segment
def bezier_fit_error(params, points):
    P0 = params[0:2]
    P1 = params[2:4]
    P2 = params[4:6]
    P3 = params[6:8]

    t_vals = np.linspace(0, 1, len(points))
    curve = np.array([bezier_curve(t, P0, P1, P2, P3) for t in t_vals])

    return np.sum(np.linalg.norm(curve - points, axis=1) ** 2)

# Fit one cubic Bézier curve to a given 2D segment of points
def fit_bezier_curve(points):
    P0 = points[0]
    P3 = points[-1]
    P1 = points[len(points)//3]
    P2 = points[2*len(points)//3]

    # Initial guess for the control points
    init = np.hstack([P0, P1, P2, P3])
    result = minimize(bezier_fit_error, init, args=(points,), method="Nelder-Mead")

    params = result.x
    return params[0:2], params[2:4], params[4:6], params[6:8]

# Split points into segments for fitting a multi-segment Bézier spline
def fit_bezier_spline(points, num_segments):
    segment_length = len(points) // num_segments
    control_points = []
    segment_errors = []

    for i in range(num_segments):
        # Define the start and end indices for the segment
        start_idx = i * segment_length
        end_idx = min((i + 1) * segment_length, len(points))

        # Fit Bézier curve for the segment
        P0, P1, P2, P3 = fit_bezier_curve(points[start_idx:end_idx])

        # Compute the error for this segment
        t_vals = np.linspace(0, 1, len(points[start_idx:end_idx]))
        curve = np.array([bezier_curve(t, P0, P1, P2, P3) for t in t_vals])
        errors = np.linalg.norm(curve - points[start_idx:end_idx], axis=1)
        rmse = np.sqrt(np.mean(errors**2))

        segment_errors.append(rmse)
        control_points.append((P0, P1, P2, P3))

        # Print error for the segment
        print(f"Segment {i + 1} RMSE: {rmse:.6f}")

    return control_points, segment_errors

# Plot Bézier spline with control points and the control polygon in 2D
def plot_bezier_spline(points, control_points):
    t = np.linspace(0, 1, 300)
    curve = []

    plt.figure(figsize=(8, 6))

    # Plot each Bézier segment
    for i, (P0, P1, P2, P3) in enumerate(control_points):
        segment_curve = np.array([bezier_curve(ti, P0, P1, P2, P3) for ti in t])
        curve.append(segment_curve)
        
        # Plot the control polygon for the segment
        control_x = [P0[0], P1[0], P2[0], P3[0]]
        control_y = [P0[1], P1[1], P2[1], P3[1]]
        plt.plot(control_x, control_y, 'k--', alpha=0.5)

    curve = np.concatenate(curve, axis=0)
    
    # Plot the whole spline
    plt.plot(curve[:, 0], curve[:, 1], "b-", label="Bézier spline")
    plt.plot(points[:, 0], points[:, 1], "ro", label="Input points")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.title("Multi-Segment Bézier Spline in 2D")
    plt.axis("equal")
    plt.show()

# Example usage with 2D points
points = np.array([
    [0, 0], [1, 0.8], [2, 0.6], [3, 1.4], [4, 1], [5, 2], [6, 1.5], [7, 2.2],
    [8, 1.8], [9, 2], [10, 1.5], [11, 2.2], [12, 1.8], [13, 2.5], [14, 3], [15, 2.8],
    [16, 3.2], [17, 3.5], [18, 3.1], [19, 2.9], [20, 2.6], [21, 2.3], [22, 2.4],
    [23, 2.5], [24, 2.8], [25, 2.3], [26, 2.6], [27, 2.9], [28, 2.5], [29, 2.7],
    [30, 2.6], [31, 2.4], [32, 2.7], [33, 2.8], [34, 3], [35, 3.3], [36, 3.2],
    [37, 3.1], [38, 3.4], [39, 3.6], [40, 3.5], [41, 3.2], [42, 3.1], [43, 2.9],
    [44, 2.8], [45, 3.0], [46, 3.1], [47, 3.3], [48, 3.2], [49, 3.5], [50, 3.6],
    [51, 3.8], [52, 3.9], [53, 3.7], [54, 3.5], [55, 3.4], [56, 3.3], [57, 3.1],
    [58, 3.0], [59, 2.9], [60, 2.8], [61, 2.9], [62, 3.0], [63, 2.8], [64, 2.6],
    [65, 2.5], [66, 2.4], [67, 2.6], [68, 2.8], [69, 2.9], [70, 2.8], [71, 3.0],
    [72, 3.1], [73, 3.2], [74, 3.3], [75, 3.2], [76, 3.4], [77, 3.5], [78, 3.6],
    [79, 3.4], [80, 3.2], [81, 3.1], [82, 3.0], [83, 2.9], [84, 3.0], [85, 3.2],
    [86, 3.3], [87, 3.5], [88, 3.6], [89, 3.8], [90, 3.9], [91, 3.8], [92, 3.7],
    [93, 3.6], [94, 3.5], [95, 3.4], [96, 3.3], [97, 3.1], [98, 3.0], [99, 2.8]
])



name = "0_-1"
import json
# 10 random points (you can replace this with your own points)
f = open(name+'/trains_'+name+'.json')
data = json.load(f)
i = 2
points = np.array([[e[0], e[1]] for e in  data["coordinates"]]) 
print(len(points))

# Fit Bézier spline to the 2D points (5 segments in this example)
num_segments = int(len(points)/10)
control_points, segment_errors = fit_bezier_spline(points, num_segments)

# Plot the 2D Bézier spline with the control points
plot_bezier_spline(points, control_points)

# Optionally, you can print the error for each segment here too:
print("\nError for each segment:")
for i, error in enumerate(segment_errors):
    print(f"Segment {i+1} RMSE: {error:.6f}")


