import cv2
import numpy as np


def image_to_canny_svg(
    image_path,
    output_svg_path,
    low_threshold=100,
    high_threshold=200,
    gaussian_blur_kernel=(1, 1),
):
    """Performs Canny edge detection on an image and saves the resulting contours

    as vector paths in an SVG file.
    """
    # 1. Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not open or find the image: {image_path}")

    height, width = img.shape[:2]

    # 2. Preprocess: Convert to grayscale and reduce noise with Gaussian Blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if gaussian_blur_kernel:
        gray = cv2.GaussianBlur(gray, gaussian_blur_kernel, 0)

    # 3. Apply Canny Edge Detection
    edges = cv2.Canny(gray, low_threshold, high_threshold)

    # 4. Extract edge outlines as continuous point paths (contours)
    # RETR_LIST retrieves all contours; CHAIN_APPROX_SIMPLE compresses horizontal,
    # vertical, and diagonal segments to leave only their end points.
    contours, _ = cv2.findContours(
        edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )

    # 5. Build and write the SVG vector file
    with open(output_svg_path, "w") as svg_file:
        # Write the SVG header with identical pixel space dimensions
        svg_file.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">\n'
        )

        # Style options: black lines, no fill, 1-pixel thickness
        path_style = 'fill="none" stroke="black" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"'

        # Loop through extracted vectors and construct SVG path components
        for contour in contours:
            if len(contour) < 2:
                continue

            # Generate standard SVG 'd' path attribute data strings
            # 'M' moves the pen to the first point; 'L' draws straight line segments to succeeding points
            points = contour.reshape(-1, 2)
            path_data = f"M {points[0][0]} {points[0][1]} "
            path_data += " ".join(f"L {x} {y}" for x, y in points[1:])

            svg_file.write(f'  <path d="{path_data}" {path_style} />\n')

        svg_file.write("</svg>\n")

    print(
        f"Successfully processed {len(contours)} edge paths! Saved to {output_svg_path}"
    )


# --- Example Execution Execution ---
if __name__ == "__main__":
    # Replace 'input.jpg' with your actual image path
    # The output file 'edges.svg' can be opened directly in any web browser or vector editor
    try:
        image_to_canny_svg(
            image_path="test1.png",
            output_svg_path="edges.svg",
            low_threshold=50,
            high_threshold=150,
        )
    except Exception as e:
        print(f"Error: {e}")
