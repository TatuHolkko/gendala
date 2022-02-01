import random
from curve import Curve
from geometry import Point
from typing import List

from utility import coinFlip

edgePadding = 0.1

def randomPoint():
    x = random.random()*2 - 1
    y = random.random()*2 - 1
    x *= 1-edgePadding
    y *= 1-edgePadding
    return Point(x,y)

def getPoints() -> List[Point]:
    edgeY = random.random()*2 - 1
    edgeY *= (1-edgePadding)
    points = []

    points.append(Point(-1,edgeY))

    points.append(randomPoint())

    if coinFlip():
        points.append(randomPoint())
    if coinFlip():
        points.append(randomPoint())
    
    points.append(Point(1, edgeY))

    return points

def extend(curve: Curve, point: Point) -> List[Point]:
    subDivs = random.randint(1,9)
    curveType = random.choice(["sine", "arc", "line"])
    if curveType == "sine":
        curve.extend(curve.sine(point, subDivs=subDivs, amplitude=random.random()-0.5))
    elif curveType == "arc":
        curve.extend(curve.arc(point, subDivs=subDivs, amplitude=random.random()*2-1))
    else:
        curve.extend(curve.line(point))

def randomCurve(closed=False) -> Curve:
    points = getPoints()
    curve = Curve(points[0],closed=closed)
    for point in points[1:]:
        extend(curve, point)
    curve.removeDuplicates()
    return curve
