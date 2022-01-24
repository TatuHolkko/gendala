from __future__ import annotations
from copy import deepcopy
import math
from utility import Line, Point, clamp, rotatePoint, shorterDistance, piWrap
from typing import List

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
            origin (Point, optional): Constant offset. Defaults to (0,0).
            startGuide (float, optional): Y axis angle at x=-1. Defaults to 0.
            endGuide (float, optional):   Y axis angle at x= 1. Defaults to 0.

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

    def __repr__(self) -> str:
        return f"{self.origin.__repr__()}, {int(self.angle/math.pi*180)}°, {self.scale}, [{int(self.startGuide/math.pi*180)}°,{int(self.endGuide/math.pi*180)}°]"

    def setYScale(self, scale:float):
        self.scale[1] = scale
    
    def getScale(self):
        return self.scale

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
            pos (Point): Offset in local coordinates
        """

        self.origin = self.getExternalPos(pos)

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

    def getExternalPos(self, pos: Point) -> Point:
        """
        Apply all transformations to a local point and return the external equivalent

        Args:
            pos (Point): Local point

        Returns:
            Point: External point
        """
        pos_ = Point(pos.x * self.scale[0], pos.y * self.scale[1])
        pos_ = self.applyPerspective(pos_)
        pos_ = rotatePoint(pos_, Point(0, 0), self.angle)
        return Point(self.origin.x + pos_.x, self.origin.y + pos_.y)

    def applyPerspective(self, point: Point) -> Point:
        """
        Apply a linear approximation of perspective transform

        Args:
            point (Point): Point to transform

        Returns:
            Point: Transformed point
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

    def apply(self, lines:List[Line]) -> List[Line]:
        """
        Apply the geospace transformations to a list of lines

        Args:
            lines (List[Line]): List of lines
            geospace (GeoSpace): Geospace to apply

        Returns:
            List[Line]: Transformed list of lines
        """
        result = []
        for line in lines:
            p1 = self.getExternalPos(line.p0)
            p2 = self.getExternalPos(line.p1)
            result.append(Line(p1, p2))
        return result
    
class GeoSpaceStack:
    """
    Coordinate space stack. Uses a reference to a coordinate space to create deep copies of it into a stack
    """
    def __init__(self):
        """
        Initialize coordinate space stack
        """
        self.stack:List[GeoSpace] = []

    def push(self, geoSpace:GeoSpace):
        """
        Push a new coordinate space into the stack
        """
        self.stack.append(deepcopy(geoSpace))

    def pop(self):
        """
        Pop the last coordinate space in stack
        :return: Coordinatespace
        """
        return self.stack.pop()
    
    def getGlobalPos(self, pos:Point) -> Point:
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