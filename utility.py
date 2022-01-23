
from __future__ import annotations
from copy import deepcopy
import math
from typing import List, Tuple
from dataclasses import dataclass


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scale: float) -> Point:
        return Point(self.x * scale, self.y * scale)
    
    def __mul__(self, other: Point) -> Point:
        return Point(self.x * other.x, self.y * other.y)
    
    def __repr__(self) -> str:
        return f"({self.x},{self.y})"
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Point):
            return False
        return self.x == __o.x and self.y == __o.y
    
    def __hash__(self) -> int:
        return int(((self.x + self.y)*(self.x + self.y + 1)/2) + self.y)


class Line:
    def __init__(self, p0:Point, p1:Point) -> None:
        self.p0 = deepcopy(p0)
        self.p1 = deepcopy(p1)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Line):
            return False
        return self.p0 == __o.p0 and self.p1 == __o.p1

    def __hash__(self) -> int:
        return self.p0.__hash__() ^ self.p1.__hash__()
    
    def __repr__(self) -> str:
        return f"({self.p0.__repr__()},{self.p1.__repr__()})"



def delta(start: Point, end: Point) -> Point:
    return Point(end.x - start.x, end.y - start.y)


def clamp(value: float, minLim: float, maxLim: float) -> float:
    return min(max(value, minLim), maxLim)


def sign(value: float) -> int:
    return int(value >= 0) * 2 - 1


def piWrap(angle: float) -> float:
    """
    Wrap angle between pi and -pi
    """
    return (angle + math.pi) % (2 * math.pi) - math.pi


def shorterDistance(angle1: float, angle2: float) -> float:
    """
    Return the shorter angle between wrapped angle1 and wrapped angle2.
    This function solves the problem where the angles have different signs
    so the subtraction results in an angle above pi.

    Args:
        angle1 (float): Angle 1
        angle2 (float): Angle 2

    Returns:
        float: shorter angular distance from angle1 to angle2
    """
    angle1 = piWrap(angle1)
    angle2 = piWrap(angle2)
    dist = abs(angle2 - angle1)

    if dist > math.pi:
        dist = 2 * math.pi - abs(angle1) - abs(angle2)
        if angle1 > angle2:
            return dist
        return -dist

    return angle2 - angle1


def angle(p1: Point, p2: Point) -> float:
    d = p2 - p1
    return math.atan2(d.y, d.x)


def innerAngle(p1: Point, p2: Point, p3: Point) -> float:
    return shorterDistance(angle(p2, p1), angle(p2, p3))


def xLimits(points: List[Point]) -> tuple[float, float]:
    resultMin = None
    resultMax = None
    for point in points:
        if resultMin is None or point.x < resultMin:
            resultMin = point.x
        if resultMax is None or point.x > resultMax:
            resultMax = point.x
    return [resultMin, resultMax]


def distance(p1: Point, p2: Point):
    d = p2 - p1
    return math.hypot(d.x, d.y)


def totalLength(points: List[Point], closed: bool = False) -> float:
    result = 0
    for i in range(len(points) - 1):
        result += distance(points[i], points[i + 1])
    if closed:
        result += distance(points[-1], points[0])
    return result


def offsetLines(lines: List[Line], deltaX: float) -> None:
    for line in lines:
        line.p0.x += deltaX
        line.p1.x += deltaX


def scaleLines(lines: List[Line], scaleX: float) -> None:
    for line in lines:
        line.p0.x *= scaleX
        line.p1.x *= scaleX


def pointsFromLines(lines: List[Line]) -> List[Point]:
    result = set()
    for line in lines:
        result.add(line.p0)
        result.add(line.p1)
    return list(result)


def normalizeLines(lines: List[Line]) -> None:
    xMin, xMax = xLimits(pointsFromLines(lines))
    width = xMax - xMin
    middle = (xMax + xMin) / 2
    scale = 2 / width
    offsetLines(lines, -middle)
    scaleLines(lines, scale)


def repeatLines(lines: List[Line], n: int) -> None:
    xMin, xMax = xLimits(pointsFromLines(lines))
    width = xMax - xMin
    result = set()
    for i in range(n):
        offset = width * i
        tempLines = deepcopy(lines)
        offsetLines(tempLines, offset)
        for line in tempLines:
            result.add(line)
    return list(result)


def tuplify(lst: List) -> tuple:
    # convert list to tuple
    return tuple(tuplify(i) if isinstance(i, list) else i for i in lst)


def listify(tpl: tuple) -> List:
    # convert tuple to list
    return list(listify(i) if isinstance(i, tuple) else i for i in tpl)


def patternFromPoints(
        lst: List[Tuple[Tuple[float, float], Tuple[float, float]]]) -> List[Line]:
    result: List[Line] = []
    for line in lst:
        result.append(
            Line(
                Point(
                    line[0][0], line[0][1]), Point(
                    line[1][0], line[1][1])))
    return result


def gradientPoint(p1: Point, p2: Point, s: float) -> Point:
    d = p2 - p1
    return Point(p1.x + d.x * s, p1.y + d.y * s)


def gradient(v1: float, v2: float, s: float) -> float:
    d = v2 - v1
    return v1 + d * s


def rotatePoint(point: Point, pivot: Point, theta: float) -> Point:
    """
    Rotate point around pivot by theta degrees

    Args:
        point (x,y): Point to rotate
        pivot (x,y): Center of rotation
        theta (float): Amount in radians

    Returns:
        (x,y): Rotated point
    """
    s = math.sin(theta)
    c = math.cos(theta)
    xr = c * (point.x - pivot.x) - s * (point.y - pivot.y) + pivot.x
    yr = s * (point.x - pivot.x) + c * (point.y - pivot.y) + pivot.y
    return Point(xr, yr)
