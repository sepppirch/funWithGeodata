import numpy as np
try:
    from noise import pnoise3
except ImportError:
    print("Please install the noise library: pip install noise")
    exit()

# Configuration
res = 20
box_size = 1.0
filename = "NoiseField.fga"

# NOISE PARAMETERS
noise_scale = 1.5  # Higher = more "wiggly" / Lower = smoother
noise_strength = 2.0 # The velocity/magnitude of the vectors

def get_noise_field(x, y, z, scale):
    # We offset the coordinates for each axis so X, Y, and Z flow differently
    # Otherwise, the vector would always be [n, n, n] (pointing 45 degrees)
    vx = pnoise3(x * scale, y * scale, z * scale, octaves=2)
    vy = pnoise3((x + 10) * scale, (y + 10) * scale, (z + 10) * scale, octaves=2)
    vz = pnoise3((x - 10) * scale, (y - 10) * scale, (z - 10) * scale, octaves=2)
    
    return np.array([vx, vy, vz]) * noise_strength

# Write the FGA file
with open(filename, "w") as f:
    f.write(f"{res}, {res}, {res},\n")
    f.write(f"-{box_size}, -{box_size}, -{box_size}, {box_size}, {box_size}, {box_size},\n")
    
    lin = np.linspace(-box_size, box_size, res)
    for z in lin:
        for y in lin:
            for x in lin:
                v = get_noise_field(x, y, z, noise_scale)
                f.write(f"{v[0]}, {v[1]}, {v[2]},\n")

print(f"Generated {filename} with scale {noise_scale}.")python