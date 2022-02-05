from __future__ import annotations
from math import atan2, cos, hypot, sin

# Float value representing radians
Angle = float
# Smallest distance allowed when detecting point location equality
collisionThreshold = 0.01

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
        if not isinstance(__o, Point):
            return False
        return self.distanceTo(__o) < collisionThreshold

    def __hash__(self) -> int:
        return int(((self.x + self.y) * (self.x + self.y + 1) / 2) + self.y)

    def angleTo(self, p: Point) -> Angle:
        d = p - self
        return atan2(d.y, d.x)

    def distanceTo(self, p: Point) -> float:
        d = p - self
        return hypot(d.x, d.y)

    def rotated(self, pivot: Point, angle: Angle) -> Point:
        s = sin(angle)
        c = cos(angle)
        xr = c * (self.x - pivot.x) - s * (self.y - pivot.y) + pivot.x
        yr = s * (self.x - pivot.x) + c * (self.y - pivot.y) + pivot.y
        return Point(xr, yr)
