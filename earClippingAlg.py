from math import atan2
 
class Point:
    """
    Class to represent a point in 2D space.
 
    Attributes:
    - x: float
        The x-coordinate of the point.
    - y: float
        The y-coordinate of the point.
    """
 
    def __init__(self, x: float, y: float):
        """
        Constructor to instantiate the Point class.
 
        Parameters:
        - x: float
            The x-coordinate of the point.
        - y: float
            The y-coordinate of the point.
        """
 
        self.x = x
        self.y = y
 
class Triangle:
    """
    Class to represent a triangle in 2D space.
 
    Attributes:
    - p1, p2, p3: Point
        The three vertices of the triangle.
    """
 
    def __init__(self, p1: Point, p2: Point, p3: Point):
        """
        Constructor to instantiate the Triangle class.
 
        Parameters:
        - p1, p2, p3: Point
            The three vertices of the triangle.
        """
 
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
 
    def is_ear(self, point: Point):
        """
        Checks if a given point is an "ear" of the triangle.
 
        Parameters:
        - point: Point
            The point to be checked.
 
        Returns:
        - bool:
            True if the point is an "ear", False otherwise.
        """
 
        # Calculate the angles formed by the point and the triangle vertices
        angle1 = self._calculate_angle(self.p1, self.p2, point)
        angle2 = self._calculate_angle(self.p2, self.p3, point)
        angle3 = self._calculate_angle(self.p3, self.p1, point)
 
        # Check if the angles are less than 180 degrees (pi radians)
        return angle1 + angle2 + angle3 < 2 * atan2(1, 0)
 
    def _calculate_angle(self, p1: Point, p2: Point, p3: Point):
        """
        Calculates the angle formed by three points.
 
        Parameters:
        - p1, p2, p3: Point
            The three points to calculate the angle.
 
        Returns:
        - float:
            The angle in radians.
        """
 
        # Calculate the vectors between the points
        v1 = Point(p1.x - p2.x, p1.y - p2.y)
        v2 = Point(p3.x - p2.x, p3.y - p2.y)
 
        # Calculate the dot product and the magnitudes of the vectors
        dot_product = v1.x * v2.x + v1.y * v2.y
        magnitude_v1 = (v1.x ** 2 + v1.y ** 2) ** 0.5
        magnitude_v2 = (v2.x ** 2 + v2.y ** 2) ** 0.5
 
        # Calculate the angle using the dot product and magnitudes
        angle = atan2(dot_product, magnitude_v1 * magnitude_v2)
 
        return angle
 
def ear_clipping(points):
    """
    Implements the ear clipping algorithm to triangulate a polygon in 2D space.
 
    Parameters:
    - points: list of Point
        The list of points representing the polygon.
 
    Returns:
    - list of Triangle:
        The list of triangles formed by the ear clipping algorithm.
    """
 
    triangles = []
 
    # Copy the points to avoid modifying the original list
    polygon = points.copy()
 
    while len(polygon) >= 3:
        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]
            p3 = polygon[(i + 2) % len(polygon)]
 
            triangle = Triangle(p1, p2, p3)
 
            is_ear = True
            for point in polygon:
                if point != p1 and point != p2 and point != p3 and triangle.is_ear(point):
                    is_ear = False
                    break
 
            if is_ear:
                triangles.append(triangle)
                polygon.remove(p2)
                break
 
    return triangles
 
# Example usage:
 
# Define the points of the polygon
points = [
    Point(0, 0),
    Point(1, 0),
    Point(1, 1),
    Point(0.5, 1.5),
    Point(0, 1)
]
 
# Triangulate the polygon using the ear clipping algorithm
print("hemlo")
triangles = ear_clipping(points)
 
# Print the triangles
for i, triangle in enumerate(triangles):
    print(f"Triangle {i + 1}:")
    print(f"  Vertex 1: ({triangle.p1.x}, {triangle.p1.y})")
    print(f"  Vertex 2: ({triangle.p2.x}, {triangle.p2.y})")
    print(f"  Vertex 3: ({triangle.p3.x}, {triangle.p3.y})")
    print()