import math
import svgwrite


def arc(svg, position, radius, rotation, start, end, color="white"):
    x0, y0 = position[0] + radius, position[1]
    x1, y1 = position[0] + radius, position[1]
    rad_start = math.radians(start % 360)
    rad_end = math.radians(end % 360)
    x0 -= (1 - math.cos(rad_start)) * radius
    y0 += math.sin(rad_start) * radius
    x1 -= (1 - math.cos(rad_end)) * radius
    y1 += math.sin(rad_end) * radius

    args = {'x0': x0,
            'y0': y0,
            'x1': x1,
            'y1': y1,
            'xradius': radius,
            'yradius': radius,
            'ellipseRotation': 0,
            'swap': 1 if end > start else 0,
            'large': 1 if abs(start - end) > 180 else 0,
    }

    # 'a/A' params: (rx,ry x-axis-rotation large-arc-flag,sweep-flag x,y)+ (case dictates relative/absolute pos)
    path = """M %(x0)f,%(y0)f
              A %(xradius)f,%(yradius)f %(ellipseRotation)f %(large)d,%(swap)d %(x1)f,%(y1)f
    """ % args
    arc = svg.path(d=path, fill="none", stroke=color, stroke_width=0.1)
    arc.rotate(rotation, position)
    svg.add(arc)

    # start/end points, just for reference
    #svg.add(svg.circle((x0, y0), r=2, stroke="green", fill="green"))
    #svg.add(svg.circle((x1, y1), r=2, stroke="red", fill="red"))


# test it
svg = svgwrite.Drawing(filename="teapot.svg", size=(400, 400))
p0 = (150, 150)



f = open("teapot.arc", "r")
for x in f:
  line = x.split()
  if line[0] == '#arc':
     arc(svg, (float(line[2])*10+150,float(line[3])*10+150), float(line[4])*10, 0, int(line[5]), int(line[6]), color="black")
#svg.add(svg.rect((100, 100), (100, 100), stroke="orange", stroke_width=1, fill="none"))
#svg.add(svg.circle(p0, r=2, stroke="orange", fill="orange"))
#arc(svg, p0, 50, 0, 90, 270, color="black")
svg.save()