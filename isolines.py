import cv2
import numpy as np
from scipy.interpolate import splprep, splev
import xml.etree.ElementTree as ET

import cv2
import numpy as np
from scipy.interpolate import splprep, splev
import xml.etree.ElementTree as ET

def dem_to_svg_contours(image_path, output_svg_path, interval=20, smoothness=0.05):
    # 1. Load the grayscale image (DEM)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not open or find the image: {image_path}")
        
    height, width = img.shape
    
    # Create the root SVG element with correct XML attributes
    svg = ET.Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'viewBox': f'0 0 {width} {height}',
        'width': str(width),
        'height': str(height),
        'style': 'background-color: #1a1a1a;' # Dark background for contrast
    })
# 2. Iterate through elevation levels
#     # 2. Iterate through elevation levels
    for level in range(interval, 255, interval):
        _, thresh = cv2.threshold(img, level, 255, cv2.THRESH_BINARY)
        
        # CLEAR THE BORDER PIXELS: Force a 1-pixel black frame around the mask
        # This breaks any white blob structure hugging the edge of the image canvas
        thresh[0, :] = 0          # Top edge
        thresh[-1, :] = 0         # Bottom edge
        thresh[:, 0] = 0          # Left edge
        thresh[:, -1] = 0         # Right edge
        
        # Find contours on the cleared mask
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        for contour in contours:
            if len(contour) < 5:
                continue
                
            points = contour.reshape(-1, 2)
            
            # CRITICAL FILTER: Identify any points sitting directly on the 1-pixel margin boundary
            # If a point is on x=1, x=width-2, y=1, or y=height-2, it's touching our artificial edge
            valid_mask = (
                (points[:, 0] > 1) & (points[:, 0] < width - 2) &
                (points[:, 1] > 1) & (points[:, 1] < height - 2)
            )
            
            # Split the contour array wherever it touches the boundary line
            diff = np.diff(valid_mask.astype(int))
            split_indices = np.where(diff != 0)[0] + 1
            
            segments = np.split(points, split_indices)
            masks = np.split(valid_mask, split_indices)
            
            for segment, mask in zip(segments, masks):
                # Only process segments that are strictly inside the interior frame
                if not np.all(mask) or len(segment) < 4: 
                    continue
                
                x = segment[:, 0]
                y = segment[:, 1]
                
                try:
                    # 3. Fit smooth parametric B-splines (per=False for open strands)
                    tck, u = splprep([x, y], s=smoothness * len(segment), per=False)
                    
                    u_new = np.linspace(0, 1, max(30, len(segment) // 2))
                    x_smooth, y_smooth = splev(u_new, tck)
                    
                    # 4. Clean open SVG path assembly (No "Z" closure)
                    path_d = f"M {x_smooth[0]:.2f},{y_smooth[0]:.2f}"
                    for i in range(1, len(x_smooth)):
                        path_d += f" L {x_smooth[i]:.2f},{y_smooth[i]:.2f}"
                    
                    # Color mapping logic
                    color_factor = level / 255.0
                    r = int(255 * color_factor)
                    g = int(200 * color_factor + 50 * (1 - color_factor))
                    b = int(255 * (1 - color_factor))
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    ET.SubElement(svg, 'path', {
                        'd': path_d,
                        'fill': 'none',
                        'stroke': hex_color,
                        'stroke-width': '1.2',
                        'stroke-linecap': 'round',
                        'stroke-linejoin': 'round',
                        'opacity': '0.85'
                    })
                    
                except Exception:
                    continue
  

    # Write out sanitized XML tree data
    tree = ET.ElementTree(svg)
    ET.indent(tree, space="  ", level=0)
    tree.write(output_svg_path, encoding='utf-8', xml_declaration=True)
    print(f"Successfully generated clean heightlines at: {output_svg_path}")


# --- Execution Example ---
if __name__ == "__main__":
    # Replace with your local terrain heightmap path
    #input_dem = "test.png" 
    input_dem = "1_-4/hmap1_-4.png" 
    output_vector = "terrain_heightlines.svg"
    
    # interval: step size between lines (smaller = more densely packed contours)
    # smoothness: higher values yield smoother shapes, lower values cling closely to jagged pixels
    dem_to_svg_contours(input_dem, output_vector, interval=1, smoothness=1.03)
