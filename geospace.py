from __future__ import annotations
import math
from utility import Line, Point, clamp, rotatePoint, shorterDistance, piWrap
from typing import List, Tuple

class GeoSpace:
    """
    A transformed coordinate space
    """

    def __init__(self, angle:float=0, xScale:float=1, yScale:float=1,
                 origin:Point=Point(0, 0), startGuide:float=0, endGuide:float=0) -> None:
        """
        Initialize the coordinate space

        Args:
            angle (float, optional): Rotation. Defaults to 0.
            xScale (float, optional): Scaling along x-axis. Defaults to 1.
            yScale (float, optional): Scaling along y-axis. Defaults to 1.
            origin (((x,y), external), optional): Constant offset. Defaults to (0,0).
            startGuide ((float), optional): Y axis angle at x=-1. Defaults to 0.
            endGuide ((float), optional):   Y axis angle at x= 1. Defaults to 0.

        The transformations are added in this order:
            Scale, perspective, rotation, offset

        The perspective works in local space between x = -1 and x = 1. If perspective is
        enabled, all points with x=[-1, 1] will get their Y axis tilted using the start and end point guides.
        Y axis direction is linearly interpolated between the start and end points.
         """
        self.angle = angle
        self.scale = [xScale, yScale]
        self.origin = origin
        self.startGuide = startGuide
        self.endGuide = endGuide

    def scaleBy(self, factor: float) -> None:
        """
        Scale both x and y by a factor

        Args:
            factor (float): Scaling factor
        """
        self.scale = [self.scale[0] * factor, self.scale[1] * factor]

    def scaleXBy(self, factor: float) -> None:
        """
        Scale x by a factor

        Args:
            factor (float): Scaling factor
        """
        self.scale[0] = self.scale[0] * factor

    def scaleYBy(self, factor: float) -> None:
        """
        Scale y by a factor

        Args:
            factor (float): Scaling factor
        """
        self.scale[1] = self.scale[1] * factor

    def rotate(self, theta: float) -> None:
        """
        Rotate the coordinate system around local origin.

        Args:
            theta (float): Angle in radians.
        """
        x_mirrored = self.scale[0] < 0
        y_mirrored = self.scale[1] < 0
        if y_mirrored and x_mirrored:
            theta = theta + math.pi
        elif y_mirrored:
            theta = -theta
        elif x_mirrored:
            theta = math.pi - theta
        self.angle += theta

    def setOrigin(self, pos: Point) -> None:
        """
        Offset the coordinate system

        Args:
            pos ((x,y), local)): Offset in local coordinates
        """

        self.origin = self.getGlobalPos(pos)

    def makeEqual(self, other:GeoSpace) -> None:
        """
        Copy all members from other.

        Args:
            other (GeoSpace): Other GeoSpace instance to copy members from
        """
        self.angle = other.angle
        self.scale = other.scale
        self.origin = other.origin
        self.startGuide = other.startGuide
        self.endGuide = other.endGuide

    def getGlobalPos(self, pos: Point) -> Point:
        """
        Apply all transformations to a local point and return the external equivalent

        Args:
            pos ((x,y), local): Local point

        Returns:
            (x,y): External point
        """
        pos_ = Point(pos.x * self.scale[0], pos.y * self.scale[1])
        pos_ = self.applyPerspective(pos_)
        pos_ = rotatePoint(pos_, Point(0, 0), self.angle)
        return Point(self.origin.x + pos_.x, self.origin.y + pos_.y)

    def applyPerspective(self, point: Point) -> Point:
        """
        Apply a linear approximation of perspective transform

        Args:
            point (x,y): Point to transform

        Returns:
            (x,y): Transformed point
        """
        s = (point.x/self.scale[0] + 1) / 2
        angle = self.angleGradient(self.startGuide, self.endGuide, s)
        x = point.x + clamp(point.y * -math.tan(angle), -100, 100)
        return Point(x, point.y)

    @staticmethod
    def angleGradient(angle1:float, angle2:float, p:float) -> float:
        """
        Return an angle [-pi, pi] that is between angle1 and angle2,
        choosing the shorter direction of travel.

        Args:
            angle1 (float): First angle
            angle2 (float): Second angle
            p (float): value between 0 and 1

        Returns:
            (float): Angle between angle1 and angle2
        """

        if abs(angle1) > math.pi or abs(angle2) > math.pi:
            raise Exception("Gradient angles not between [-pi,pi]")

        delta = shorterDistance(angle1, angle2)
        result = piWrap(angle1 + p * delta)
        return result

def applyGeospace(lines: List[Line], geospace: GeoSpace) -> List[Line]:
    result = []
    for line in lines:
        p1 = geospace.getGlobalPos(line.p0)
        p2 = geospace.getGlobalPos(line.p1)
        result.append(Line(p1, p2))
    return result