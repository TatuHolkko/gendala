import math
import copy
from typing import Tuple


class GeoSpace:
    """
    A transformed coordinate space
    """

    def __init__(self, angle=0, xScale=1, yScale=1,
                 origin=(0, 0), shrinkPoint=(0, 0)) -> None:
        """
        Initialize the coordinate space

        Args:
            angle (float, optional): Rotation. Defaults to 0.
            xScale (float, optional): Scaling along x-axis. Defaults to 1.
            yScale (float, optional): Scaling along y-axis. Defaults to 1.
            origin (((x,y), external), optional): Constant offset. Defaults to (0,0).
            shrinkPoint (((x,y), local), oprtional): Perspective point. Defaults to (0,0).

        The transformations are added in this order:
            Perspective, scale, rotation, offset

        If the shrinkpoint is at (0,0), it has no effect. All points after the shrinkpoint
        (away from origin) are clamped to the shrink point.

        """
        self.angle = angle
        self.scale = [xScale, yScale]
        self.origin = origin
        self.shrinkPoint = shrinkPoint

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
        self.shrinkPoint = other.shrinkPoint

    def getGlobalPos(self, pos: Tuple) -> Tuple:
        """
        Apply all transformations to a local point and return the external equivalent

        Args:
            pos ((x,y), local): Local point

        Returns:
            (x,y): External point
        """
        if self.shrinkPoint is not [0, 0]:
            yLimit = self.shrinkPoint[1]
            pos = self.gradientPoint(
                (pos[0], 0), self.shrinkPoint, self.yClamp(pos)[1] / yLimit)
        x, y = self.rotate_point((pos[0] * self.scale[0],
                                  pos[1] * self.scale[1]),
                                 (0, 0),
                                 self.angle)
        return self.origin[0] + x, self.origin[1] + y

    def yClamp(self, p: Tuple) -> Tuple:
        """
        Clamp the point p so that it does not cross the shrink point

        Args:
            p (x,y): Point to clamp

        Returns:
            (x,y): Point that is either at the shrink point or on the origin side of it
        """
        if self.shrinkPoint[1] < 0:
            return (p[0], max(self.shrinkPoint[1], p[1]))
        return (p[0], min(self.shrinkPoint[1], p[1]))

    @staticmethod
    def gradientPoint(p0: Tuple, p1: Tuple, s: float) -> Tuple:
        """
        Get a point between p0 and p1.

        Args:
            p0 (x,y): point 0
            p1 (x,y): point 1
            s (float): float between 0 and 1 specifying the point between p0 and p1

        Returns:
            (x, y): Point between p0 and p1
        """
        delta = (p1[0] - p0[0], p1[1] - p0[1])
        x = p0[0] + delta[0] * s
        y = p0[1] + delta[1] * s
        return (x, y)

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
        xr = c * (point[0] - pivot[0]) - s * (point[1] - pivot[1]) + point[0]
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
