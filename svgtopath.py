from svgpathtools import svg2paths
from svgpathtools import CubicBezier, QuadraticBezier

def parse_svg_beziers(svg_file):
    paths, attributes = svg2paths(svg_file)

    bezier_data = []

    for path in paths:
        for segment in path:
            if isinstance(segment, CubicBezier):
                bezier_data.append([segment.start.real/10000, segment.start.imag/10000])
                bezier_data.append([segment.control1.real/10000,segment.control1.imag/10000])
                bezier_data.append([segment.control2.real/10000,segment.control2.imag/10000])


            elif isinstance(segment, QuadraticBezier):
                bezier_data.append({
                    "type": "quadratic",
                    "start": (segment.start.real/10000, segment.start.imag/10000),
                    "control": (segment.control.real/10000, segment.control.imag/10000),
                    "end": (segment.end.real/10000, segment.end.imag/10000),
                })

    return bezier_data

import json
if __name__ == "__main__":
    svg_path = "test.svg"
    beziers = parse_svg_beziers(svg_path)

    for b in beziers:
        print(b)

    thisbezier =json.dumps({"points":beziers})
#print(Tin)

    with open("F:/CLOUDBASE_git/Content/data/json/splines/bezier_X30_Y16.json", "w") as outfile:
        outfile.write(thisbezier)
