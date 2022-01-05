import math
from utility import clamp, shorterDistance, piWrap
from typing import Tuple


class GeoSpace:
    """
    A transformed coordinate space
    """

    def __init__(self, angle=0, xScale=1, yScale=1,
                 origin=(0, 0), startGuide=0, endGuide=0) -> None:
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

    def setOrigin(self, pos: Tuple) -> None:
        """
        Offset the coordinate system

        Args:
            pos ((x,y), local)): Offset in local coordinates
        """

        self.origin = self.getGlobalPos(pos)

    def makeEqual(self, other) -> None:
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

    def getGlobalPos(self, pos: Tuple) -> Tuple:
        """
        Apply all transformations to a local point and return the external equivalent

        Args:
            pos ((x,y), local): Local point

        Returns:
            (x,y): External point
        """
        pos_ = [pos[0] * self.scale[0], pos[1] * self.scale[1]]
        pos_ = self.applyPerspective(pos_)
        x, y = self.rotate_point(pos_, (0, 0), self.angle)
        return self.origin[0] + x, self.origin[1] + y

    def applyPerspective(self, point: Tuple) -> Tuple:
        """
        Apply a linear approximation of perspective transform

        Args:
            point (x,y): Point to transform

        Returns:
            (x,y): Transformed point
        """
        s = (point[0]/self.scale[0] + 1) / 2
        angle = self.angleGradient(self.startGuide, self.endGuide, s)
        x = point[0] + clamp(point[1] * -math.tan(angle), -100, 100)
        return (x, point[1])

    @staticmethod
    def angleGradient(angle1, angle2, p):
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

    @staticmethod
    def rotate_point(point: Tuple, pivot: Tuple, theta: float):
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
        xr = c * (point[0] - pivot[0]) - s * (point[1] - pivot[1]) + pivot[0]
        yr = s * (point[0] - pivot[0]) + c * (point[1] - pivot[1]) + pivot[1]
        return [xr, yr]


class GeoSpaceStack:
    """
    Coordinate space stack. Uses a reference to a coordinate space to create deep copies of it into a stack
    """

    def __init__(self, coordinatespace: GeoSpace) -> None:
        """
        Initialize the stack

        Args:
            coordinatespace (GeoSpace): Reference to a coordinate space
        """
        self.local = coordinatespace
        self.stack = []

    def push(self) -> None:
        """
        Push a copy of the current coordinate space to the stack
        """
        self.stack.append(copy.deepcopy(self.local))

    def revert(self) -> None:
        """
        Overwrite current coordinate space using the top of the stack
        """
        self.local.make_equal(self.stack[-1])

    def pop(self) -> None:
        """
        Pop the last coordinate space

        Returns:
            GeoSpace: Coordinate space
        """
        return self.stack.pop()
