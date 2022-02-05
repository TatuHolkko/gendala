import random
from common.utility import coinFlip
from hierarchy.curve import Curve
from geometry.point import Point
from typing import List

edgePadding = 0.1


def randomPoint():
    x = random.random() * 2 - 1
    y = random.random() * 2 - 1
    x *= 1 - edgePadding
    y *= 1 - edgePadding
    return Point(x, y)


def randomCoordinate():
    return (random.random() * 2 - 1) * (1 - edgePadding)


def getPoints() -> List[Point]:
    points = []
    continuous = coinFlip()
    edgeY = randomCoordinate()

    if continuous:
        points.append(Point(-1, edgeY))

    if coinFlip():
        points.append(randomPoint())
    if coinFlip():
        points.append(randomPoint())
    if coinFlip():
        points.append(randomPoint())

    if not continuous and len(points) < 2:
        points.append(randomPoint())
        points.append(randomPoint())

    if continuous:
        points.append(Point(1, edgeY))

    return points


def extend(curve: Curve, point: Point) -> List[Point]:
    subDivs = random.randint(1, 9)
    curveType = random.choice(["sine", "arc", "line"])
    if curveType == "sine":
        curve.extend(
            curve.sine(
                point,
                subDivs=subDivs,
                amplitude=random.random() -
                0.5))
    elif curveType == "arc":
        curve.extend(
            curve.arc(
                point,
                subDivs=subDivs,
                amplitude=random.random() *
                2 -
                1))
    else:
        curve.extend(curve.line(point))


def randomCurve(closed=False) -> Curve:
    points = getPoints()
    curve = Curve(points[0], closed=closed)
    for point in points[1:]:
        extend(curve, point)
    curve.removeDuplicates()
    if (len(curve.points) < 2) or (len(curve.points) < 3 and closed):
        # if all random points landed on top of each other
        return randomCurve(closed=closed)
    return curve
