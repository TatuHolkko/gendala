from __future__ import annotations
from copy import deepcopy
from math import atan2, cos, hypot, pi, sin
from textwrap import wrap
from typing import List

#Float value representing radians
Angle = float

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

    def __repr__(self) -> str:
        return f"({self.x:.2f},{self.y:.2f})"

    def __eq__(self, __o: object) -> bool:
        return self is __o

    def __hash__(self) -> int:
        return int(((self.x + self.y) * (self.x + self.y + 1) / 2) + self.y)

    def angleTo(self, p: Point) -> Angle:
        d = p - self
        return atan2(d.y, d.x)

    def distanceTo(self, p: Point) -> float:
        d = p - self
        return hypot(d.x, d.y)

    def rotate(self, pivot: Point, angle: Angle) -> Point:
        s = sin(angle)
        c = cos(angle)
        xr = c * (self.x - pivot.x) - s * (self.y - pivot.y) + pivot.x
        yr = s * (self.x - pivot.x) + c * (self.y - pivot.y) + pivot.y
        return Point(xr, yr)


class Line:
    def __init__(self, p0: Point, p1: Point) -> None:
        self.p0 = p0
        self.p1 = p1
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Line):
            return False
        return self.p0 == __o.p0 and self.p1 == __o.p1

    def __hash__(self) -> int:
        return self.p0.__hash__() ^ self.p1.__hash__()

    def __repr__(self) -> str:
        return f"({self.p0.__repr__()},{self.p1.__repr__()})"


class Pattern:
    def __init__(self) -> None:
        self.lines: set[Line] = set()
        self.points: set[Point] = set()
        self.xMin = 0
        self.xMax = 0
        self.yMin = 0
        self.yMax = 0

    def add(self, line: Line) -> None:
        self.lines.add(line)
        self.points.add(line.p0)
        self.points.add(line.p1)
        self.updateLimits(line.p0)
        self.updateLimits(line.p1)

    def combine(self, other:Pattern) -> None:
        for line in other.lines:
            self.add(line)

    def updateLimits(self, point: Point = None) -> None:
        
        if point is None:
            self.xMax = 0
            self.xMin = 0
            self.yMax = 0
            self.yMin = 0
            for point in self.points:
                self.updateLimits(point)
        
        self.xMax = max(self.xMax, point.x)
        self.xMin = min(self.xMin, point.x)
        self.yMax = max(self.yMax, point.y)
        self.yMin = min(self.yMin, point.y)

    def getWidth(self) -> float:
        self.updateLimits()
        return self.xMax - self.xMin

    def normalizeX(self) -> None:
        width = self.getWidth()
        middle = (self.xMax + self.xMin) / 2
        scale = 2 / width
        self.offsetX(-middle)
        self.scaleX(scale)

    def offsetX(self, deltaX: float) -> None:
        for p in self.points:
            p.x += deltaX

    def scaleX(self, scaleX: float) -> None:
        for p in self.points:
            p.x *= scaleX

    def repeat(self, n: int) -> None:
        width = 2
        newSet = Pattern()
        for i in range(n-1):
            offset = width * (i+1)
            for line in self.lines:
                newLine = deepcopy(line)
                newLine.p0.x += offset
                newLine.p1.x += offset
                newSet.add(newLine)
        for newLine in newSet.lines:
            self.add(newLine)
    
    def __repr__(self) -> str:
        return self.lines.__repr__()


def deg(a: Angle) -> float:
    return a * 180 / pi


def wrap(a: Angle) -> Angle:
    """
    Wrap angle between pi and -pi

    Args:
        value (float): Angle to wrap

    Returns:
        float: Angle between pi and -pi
    """
    return (a + pi) % (2 * pi) - pi


def convexAngle(a1: Angle, a2: Angle) -> Angle:
    """
    Return the smaller angle between the given angles.
    This function solves the problem where the angles have different signs
    so the subtraction results in an angle above pi.

    Args:
        a1 (Angle): First angle
        a2 (Angle): Second angle

    Returns:
        Angle: Angle a2-a1, chosen on the side that is below pi
    """
    angle1 = wrap(a1)
    angle2 = wrap(a2)
    dist = abs(angle2 - angle1)

    if dist > pi:
        dist = 2 * pi - abs(angle1) - abs(angle2)
        if angle1 > angle2:
            return dist
        return -dist

    return angle2 - angle1


def cornerAngle(p1: Point, corner: Point, p2: Point) -> Angle:
    """
    Return the sharp angle at corner

    The angle is the inner angle at "corner" in a triangle p1-corner-p3

    Args:
        p1 (Point): First connection point
        corner (Point): Corner point at which the angle is measured
        p2 (Point): Second connection point

    Returns:
        Angle: Sharp angle at the corner
    """
    return convexAngle(corner.angleTo(p1), corner.angleTo(p2))



