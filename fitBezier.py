import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Helper function: Cubic Bézier curve in 2D
def bezier_curve(t, P0, P1, P2, P3):
    return ((1 - t)**3 * P0 +
            3 * (1 - t)**2 * t * P1 +
            3 * (1 - t) * t**2 * P2 +
            t**3 * P3)

# Helper function: Fit cubic Bézier curve to a 2D segment with tangent continuity
def bezier_fit_error(params, points, max_control_dist=2.0, penalty_strength=10.0):
    P0 = params[0:2]
    P1 = params[2:4]
    P2 = params[4:6]
    P3 = params[6:8]
    
    # Compute distance between P1 and P2
    control_dist = np.linalg.norm(P1 - P2)

    # Add penalty if the distance between P1 and P2 exceeds max_control_dist
    penalty = 0
    if control_dist > max_control_dist:
        penalty = penalty_strength * (control_dist - max_control_dist)**2  # stronger quadratic penalty

    # Compute the Bézier curve error (least squares)
    t_vals = np.linspace(0, 1, len(points))
    curve = np.array([bezier_curve(t, P0, P1, P2, P3) for t in t_vals])
    curve_error = np.sum(np.linalg.norm(curve - points, axis=1) ** 2)

    return curve_error + penalty  # Total error with penalty

# Function to fit Bézier spline with tangent and position continuity
def fit_bezier_spline_with_continuity(points, num_segments, max_control_dist=2.0, penalty_strength=10.0):
    segment_length = len(points) // num_segments
    control_points = []
    segment_errors = []

    for i in range(num_segments):
        # Define the start and end indices for the segment
        start_idx = i * segment_length
        end_idx = min((i + 1) * segment_length, len(points))

        # If it's not the first segment, enforce continuity with the previous segment

        
        P0 = points[start_idx]
        P3 = points[end_idx]

        if i > 0:
            # Ensure continuity of position and tangent between segments
            v1 = np.subtract(P0,control_points[i-1][2])

            P1 = control_points[i-1][3]  # P2 from previous segment
            P2 = P1+v1  # P3 from previous segment
        else:
            # For the first segment, initialize normally
            P1 = points[len(points)//3]
            P2 = points[2*len(points)//3]

        # Fit Bézier curve for the segment with distance limit and tangent continuity
        init = np.hstack([P0, P1, P2, P3])
        result = minimize(bezier_fit_error, init, args=(points[start_idx:end_idx], max_control_dist, penalty_strength), method="Nelder-Mead")

        # Update control points after optimization
        P0, P1, P2, P3 = result.x[:2], result.x[2:4], result.x[4:6], result.x[6:8]

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



# Fit Bézier spline to the 2D points (5 segments in this example), with max control distance

name = "0_-1"
import json
# 10 random points (you can replace this with your own points)
f = open(name+'/trains_'+name+'.json')
data = json.load(f)
i = 2
points = np.array([[e[0], e[1]] for e in  data["coordinates"]]) 
print(len(points))

# Fit Bézier spline to the 2D points (5 segments in this example)
num_segments = int(len(points)/20)

max_control_dist = 1  # Maximum allowed distance between P1 and P2 in each segment
control_points, segment_errors = fit_bezier_spline_with_continuity(points, num_segments, max_control_dist)

# Plot the 2D Bézier spline with the control points
plot_bezier_spline(points, control_points)

# Optionally, print the error for each segment
print("\nError for each segment:")
for i, error in enumerate(segment_errors):
    print(f"Segment {i+1} RMSE: {error:.6f}")

