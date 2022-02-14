from __future__ import annotations
from multipledispatch import dispatch
from copy import deepcopy
import math
from common.utility import clamp, gradient
from geometry.point import Point
from geometry.line import Line
from geometry.utility import Angle, convexAngle
from hierarchy.pattern import Pattern
from typing import List


class GeoSpace:
    """
    A transformed coordinate space
    """

    def __init__(
            self,
            angle: Angle = Angle(0),
            xScale: float = 1,
            yScale: float = 1,
            origin: Point = Point(
                0,
                0),
            startAngle: Angle = 0,
            endAngle: Angle = 0,
            startScale: float = 1,
            endScale: float = 1) -> None:
        """
        Initialize the coordinate space

        Args:
            angle (Angle, optional): Rotation. Defaults to 0.
            xScale (float, optional): Scaling along x-axis. Defaults to 1.
            yScale (float, optional): Scaling along y-axis. Defaults to 1.
            origin (Point, optional): Constant offset. Defaults to (0,0).
            startAngle (Angle, optional): Y axis angle at x=-1. Defaults to 0.
            endAngle (Angle, optional):   Y axis angle at x= 1. Defaults to 0.
            startScale (float, optional): Y scaling at the start. Defaults to 1.
            endScale (float, optional): Y scaling at the end. Defaults to 1.

        The transformations are added in this order:
            Scale, perspective, rotation, offset

        The perspective works in local space between x = -1 and x = 1. If perspective is
        enabled, all points with x=[-1, 1] will get their Y axis tilted using the start and end point angles.
        Y axis direction is linearly interpolated between the start and end points.
         """
        self.angle = angle
        self.scale = [xScale, yScale]
        self.origin = origin
        self.startAngle = startAngle
        self.endAngle = endAngle
        self.startScale = startScale
        self.endScale = endScale

    def __repr__(self) -> str:
        return f"{self.origin.__repr__()}, {int(self.angle/math.pi*180)}°, {self.scale}, [{int(self.startAngle/math.pi*180)}°,{int(self.endAngle/math.pi*180)}°]"

    def getExternalPos(self, pos: Point) -> Point:
        """
        Apply all transformations to a local point and return the external equivalent

        Args:
            pos (Point): Local point

        Returns:
            Point: External point
        """
        pos_ = Point(pos.x * self.scale[0], pos.y * self.scale[1])
        self.applyPerspective(pos_)
        pos_ = pos_.rotated(Point(0, 0), self.angle)
        pos_.x += self.origin.x
        pos_.y += self.origin.y
        return pos_

    def applyPerspective(self, point: Point) -> None:
        """
        Apply a linear approximation of perspective transform

        Args:
            point (Point): Point to transform
        """
        s = (point.x / self.scale[0] + 1) / 2
        yScale = gradient(self.startScale, self.endScale, s)
        angle = self.angleGradient(self.startAngle, self.endAngle, s)
        point.x = point.x + \
            clamp(yScale * point.y * -math.tan(angle), -100, 100)
        point.y *= yScale

    @staticmethod
    def angleGradient(angle1: Angle, angle2: Angle, p: float) -> Angle:
        """
        Return an angle [-pi, pi] that is between angle1 and angle2,
        choosing the shorter direction of travel.

        Args:
            angle1 (Angle): First angle
            angle2 (Angle): Second angle
            p (float): value between 0 and 1

        Returns:
            (Angle): Angle between angle1 and angle2
        """

        delta = convexAngle(angle1, angle2)
        result = (angle1 + p * delta)
        return result

    @dispatch(Pattern)
    def transform(self, pattern: Pattern) -> None:
        """
        Apply this GeoSpace to the given pattern

        Args:
            pattern (Pattern): Pattern to transform
        """
        points = set()
        for line in pattern.lines:
            points.add(line.p0)
            points.add(line.p1)
        for point in points:
            self.transform(point)

    @dispatch(Line)
    def transform(self, line: Line) -> None:
        """
        Apply this GeoSpace to the given line

        Args:
            line (Line): Line to transform
        """
        self.transform(line.p0)
        if line.p0 is not line.p1:
            self.transform(line.p1)

    @dispatch(Point)
    def transform(self, point: Point) -> None:
        """
        Apply this GeoSpace to the given point

        Args:
            point (Point): Point to transform
        """
        newPoint = self.getExternalPos(point)
        point.x = newPoint.x
        point.y = newPoint.y


class GeoSpaceStack:
    """
    Coordinate space stack.
    """

    def __init__(self):
        """
        Initialize coordinate space stack
        """
        self.stack: List[GeoSpace] = []

    def push(self, geoSpace: GeoSpace):
        """
        Push a new coordinate space into the stack
        """
        self.stack.append(deepcopy(geoSpace))

    def pop(self) -> GeoSpace:
        """
        Return the top GeoSpace and remove it from the stack

        Returns:
            GeoSpace: Top most GeoSpace
        """
        return self.stack.pop()

    def getGlobalPos(self, pos: Point) -> Point:
        """
        Apply the whole stack of geospaces to get the global position

        Args:
            pos (Point): Local point in the top most geospace

        Returns:
            Point: Global point
        """
        newPos = deepcopy(pos)
        for geoSpace in reversed(self.stack):
            newPos = geoSpace.getExternalPos(newPos)
        return newPos


def geoSpaceBetween(p0: Point, p1: Point) -> GeoSpace:
    """
    Create a GeoSpace between two points

    Args:
        p0 (Point): First point
        p1 (Point): Second point

    Returns:
        GeoSpace: GeoSpace between the points
    """
    scale = p0.distanceTo(p1) / 2
    angle_ = p0.angleTo(p1)
    midpoint = gradient(p0, p1, 0.5)
    return GeoSpace(angle_, scale, scale, midpoint)
