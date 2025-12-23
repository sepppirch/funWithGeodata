import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def bezier_curve(t, P0, P1, P2, P3):
    return ((1 - t)**3 * P0 +
            3 * (1 - t)**2 * t * P1 +
            3 * (1 - t) * t**2 * P2 +
            t**3 * P3)

def bezier_fit_error(params, points):
    P0 = params[0:2]
    P1 = params[2:4]
    P2 = params[4:6]
    P3 = params[6:8]

    t_vals = np.linspace(0, 1, len(points))
    curve = np.array([bezier_curve(t, P0, P1, P2, P3) for t in t_vals])

    return np.sum((curve - points) ** 2)

def fit_bezier_curve(points):
    P0 = points[0]
    P3 = points[-1]
    P1 = points[len(points)//3]
    P2 = points[2*len(points)//3]

    init = np.hstack([P0, P1, P2, P3])
    result = minimize(bezier_fit_error, init, args=(points,), method="Nelder-Mead")

    params = result.x
    return params[0:2], params[2:4], params[4:6], params[6:8]

def compute_fit_metrics(points, P0, P1, P2, P3):
    t_vals = np.linspace(0, 1, len(points))
    curve = np.array([bezier_curve(t, P0, P1, P2, P3) for t in t_vals])

    errors = np.linalg.norm(curve - points, axis=1)

    rmse = np.sqrt(np.mean(errors ** 2))
    mean_error = np.mean(errors)
    max_error = np.max(errors)

    return rmse, mean_error, max_error

def plot_bezier_with_control_points(points, P0, P1, P2, P3, metrics):
    t = np.linspace(0, 1, 300)
    curve = np.array([bezier_curve(ti, P0, P1, P2, P3) for ti in t])

    control_x = [P0[0], P1[0], P2[0], P3[0]]
    control_y = [P0[1], P1[1], P2[1], P3[1]]

    rmse, mean_error, max_error = metrics

    plt.figure(figsize=(9, 6))
    plt.plot(points[:, 0], points[:, 1], "ro", label="Input points")
    plt.plot(curve[:, 0], curve[:, 1], "b-", linewidth=2, label="Bézier curve")

    plt.plot(control_x, control_y, "k--", label="Control polygon")
    plt.scatter(control_x, control_y, c="black", s=60)

    for i, P in enumerate([P0, P1, P2, P3]):
        plt.text(P[0], P[1], f"P{i}", fontsize=12, ha="right")

    plt.title(
        "Cubic Bézier Fit\n"
        f"RMSE = {rmse:.4f}, Mean Error = {mean_error:.4f}, Max Error = {max_error:.4f}"
    )

    plt.axis("equal")
    plt.legend()
    plt.show()

# Example usage


name = "0_-1"
import json
# 10 random points (you can replace this with your own points)
f = open(name+'/rail_'+name+'.json')
data = json.load(f)
i = 2
points = np.array([[e[0], e[1]] for e in  data["features"][i]["geometry"]["coordinates"]]) 
print(len(data["features"][i]["geometry"]["coordinates"]))



P0, P1, P2, P3 = fit_bezier_curve(points)
metrics = compute_fit_metrics(points, P0, P1, P2, P3)
plot_bezier_with_control_points(points, P0, P1, P2, P3, metrics)

print("Fit quality:")
print(f"  RMSE       : {metrics[0]:.6f}")
print(f"  Mean error : {metrics[1]:.6f}")
print(f"  Max error  : {metrics[2]:.6f}")





print(P0)
print(P1)
print(P2)
print(P3)
