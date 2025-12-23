import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt



def bezier_curve(t, P0, P1, P2, P3):
    """Compute the cubic Bezier curve at time t given 4 control points P0, P1, P2, P3."""
    return (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

def bezier_fit_error(params, points):
    """Calculate the sum of squared errors between the Bézier curve and the points."""
    # Extract control points from the params
    P0 = np.array([params[0], params[1]])
    P1 = np.array([params[2], params[3]])
    P2 = np.array([params[4], params[5]])
    P3 = np.array([params[6], params[7]])
    
    # Generate t values (between 0 and 1) corresponding to the 10 points
    t_values = np.linspace(0, 1, len(points))
    
    # Compute the Bézier curve points
    bezier_points = np.array([bezier_curve(t, P0, P1, P2, P3) for t in t_values])
    
    # Compute the squared error between the Bézier curve and the given points
    error = np.sum((bezier_points - points)**2)
    return error

def fit_bezier_curve(points):
    """Fit a cubic Bézier curve to the given points using optimization."""
    # Initial guess for the control points (P0, P1, P2, P3)
    # Start with a reasonable guess such as the first, last, and midpoints of the points
    P0_init = points[0]
    P3_init = points[-1]
    P1_init = points[len(points) // 3]
    P2_init = points[2 * len(points) // 3]
    
    # Flatten the initial control points into a 1D array
    initial_params = np.array([*P0_init, *P1_init, *P2_init, *P3_init])
    
    # Use scipy's minimize function to find the optimal control points
    result = minimize(bezier_fit_error, initial_params, args=(points,), method='Nelder-Mead')
    
    # The optimized control points
    optimized_params = result.x
    P0_opt = np.array([optimized_params[0], optimized_params[1]])
    P1_opt = np.array([optimized_params[2], optimized_params[3]])
    P2_opt = np.array([optimized_params[4], optimized_params[5]])
    P3_opt = np.array([optimized_params[6], optimized_params[7]])
    
    return P0_opt, P1_opt, P2_opt, P3_opt

def plot_curve(points, P0, P1, P2, P3):
    """Plot the Bézier curve and the original points."""
    t_values = np.linspace(0, 1, 100)
    bezier_points = np.array([bezier_curve(t, P0, P1, P2, P3) for t in t_values])
    
    # Plot the points and the curve
    plt.plot(points[:, 0], points[:, 1], 'ro', label='Data points')
    plt.plot(bezier_points[:, 0], bezier_points[:, 1], 'b-', label='Fitted Bézier curve')
    plt.legend()
    plt.title('Best-Fitting Bézier Curve')
    plt.show()

# Example usage:
name = "0_-1"
import json
# 10 random points (you can replace this with your own points)
f = open(name+'/roadssmooth_'+name+'.json')
data = json.load(f)

points = np.array([[e[0], e[1]] for e in  data["features"][5]["geometry"]["coordinates"]]) 
print(len(data["features"][5]["geometry"]["coordinates"]))


# Fit the Bézier curve
P0, P1, P2, P3 = fit_bezier_curve(points)

# Plot the results
plot_curve(points, P0, P1, P2, P3)
