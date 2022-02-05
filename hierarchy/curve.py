
from copy import deepcopy
from math import atan, pi, sin, tan
from typing import List, Tuple
from common.utility import clamp, gradient
from geometry.line import Line
from geometry.point import Point
from geometry.geospace import GeoSpace
from geometry.utility import cornerAngle
from hierarchy.pattern import Pattern

# Smallest angle allowed when detecting too sharp angles
parallelAngleThreshold = 20 / 360 * 2 * pi


class GeometryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Curve():
    """
    Curve is a continuous series of points, defined by simple shapes
    """

    def __init__(self, start: Point, closed: bool = False) -> None:
        """Intialize the class

        Args:
            start (Point): Starting point
            closed (bool, optional): Whether the curve is a closed loop. Defaults to False.
        """
        self.points = [start]
        self.start = self.points[0]
        self.end = self.points[0]
        self.closed = closed

    def __repr__(self) -> str:
        return "[" + ",".join([p.__repr__() for p in self.points]) + "]"

    def extend(self, points: List[Point]) -> None:
        """
        Add a list of points to the curve

        Args:
            points (List[Point]): Points to add
        """
        self.points.extend(points)
        self.end = points[-1]
        if self.end == self.start:
            self.closed = True
            self.points.pop()
            self.end = self.points[-1]

    def getPoints(self) -> List[Point]:
        """
        Get points of this curve

        Returns:
            List[Point]: Points
        """
        return self.points

    def getPattern(self) -> Pattern:
        """
        Create Pattern from this curve

        Returns:
            Pattern: Pattern from points of this curve
        """
        result = Pattern()
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            result.add(Line(p1, p2))
        if self.closed:
            result.add(Line(self.points[-1], self.points[0]))
        return result

    def sharpCorners(self, minAngle: float) -> List[int]:
        """
        Get a list of indices of points, which cause a sharp corner in the curve

        Args:
            minAngle (float): Minimum angle between adjacent lines

        Returns:
            List[int]: Indices of the sharp corners
        """
        result: List[int] = []

        if self.closed:
            p1 = self.points[-1]
            p2 = self.points[0]
            p3 = self.points[1]
            angle_ = cornerAngle(p1, p2, p3)
            if abs(angle_) <= minAngle:
                result.append(0)

        for i in range(len(self.points) - 2):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            p3 = self.points[i + 2]
            angle_ = cornerAngle(p1, p2, p3)
            if abs(angle_) <= minAngle:
                result.append(i + 1)

        if self.closed:
            p1 = self.points[-2]
            p2 = self.points[-1]
            p3 = self.points[0]
            angle_ = cornerAngle(p1, p2, p3)
            if abs(angle_) <= minAngle:
                result.append(len(self.points) - 1)

        return result

    def round(self, minAngle: float = pi / 2) -> None:
        """
        Replace sharp corners with pairs of less sharp corners

        If an angle between adjacent lines is smaller than minAngle, it is considered sharp.
        Points at sharp corners are removed from the curve, and replaced with two points, which
        are placed along the lines of the corner. If the resulting two shallower angles are still
        sharp, the process is repeated.

        Args:
            minAngle (float, optional): Minimum angle between adjacent lines. Defaults to pi/2.
        """
        pointsToRound = self.sharpCorners(minAngle)
        while pointsToRound:
            rounds: List[Tuple[int, Tuple[Point, Point]]] = []
            for point in pointsToRound:
                rounds.append([point, self.roundPoint(point)])
            indexOffset = 0
            for round in rounds:
                index = round[0] + indexOffset
                points = round[1]
                self.points[index].x = points[1].x
                self.points[index].y = points[1].y
                self.points.insert(index, deepcopy(points[0]))
                indexOffset += 1
            self.removeDuplicates()
            if (len(self.points) < 2) or (
                    len(self.points) < 3 and self.closed):
                raise GeometryException("Curve not roundable.")
            pointsToRound = self.sharpCorners(minAngle)

    def roundPoint(self, i: int) -> Tuple[Point, Point]:
        """
        Return points that should replace the point at index i in order
        to remove the sharp corner at index i.

        Args:
            i (int): Index of the sharp corner

        Returns:
            Tuple[Point, Point]: Two points to be inserted in the curce
        """
        p1 = self.points[i - 1]
        p2 = self.points[i]
        p3 = self.points[(i + 1) % len(self.points)]
        d1 = p2.distanceTo(p1)
        d2 = p2.distanceTo(p3)
        d = min(d1, d2)
        rounded1 = gradient(p2, p1, 0.3 * (d / d1))
        rounded2 = gradient(p2, p3, 0.3 * (d / d2))
        return (rounded1, rounded2)

    def removeDuplicates(self):
        toRemove: List[int] = []
        for i in range(len(self.points)):
            if i == len(self.points) - 1 and not self.closed:
                break
            nextIndex = (i + 1) % len(self.points)
            p1 = self.points[i]
            p2 = self.points[nextIndex]
            if p1 == p2:
                toRemove.append(nextIndex)
        for i in sorted(toRemove, reverse=True):
            self.points.pop(i)

    def sine(self,
             end: Point,
             subDivs: int = 15,
             amplitude: float = 0.2) -> List[Point]:
        """
        Generate points that define a single sine wave from current endpoint
        to given new endpoint. The current endpoint (and the starting point of this sine wave)
        is not included in the returned list.

        Args:
            end (Point): New endpoint of the curve
            subDivs (int, optional): Number of points between the start and the end. Defaults to 15.
            amplitude (float, optional): Amplitude of the sine wave. Defaults to 0.2.

        Returns:
            List[Point]: Points along the sine wave
        """

        result: List[Point] = []
        gspace = geoSpaceBetween(self.end, end)
        for i in range(subDivs):
            p = (i + 1) / (subDivs + 1)
            phi = 2 * pi * p
            x = 2 * p - 1
            subDivPoint = gspace.getExternalPos(Point(x, sin(phi) * amplitude))
            result.append(subDivPoint)
        result.append(deepcopy(end))
        return result

    def line(self,
             end: Point,
             subDivs: int = 0) -> List[Point]:
        """
        Generate points along a line between current endpoint and the given endpoint.

        Args:
            end (Point): New endpoint of the curve
            subDivs (int, optional): Number of points between the start and the end. Defaults to 0.

        Returns:
            List[Point]: Points along the line
        """

        result: List[Point] = []

        for i in range(subDivs):
            p = (i + 1) / (subDivs + 1)
            gradPoint = gradient(self.end, end, p)
            result.append(gradPoint)

        result.append(deepcopy(end))
        return result

    def arc(self,
            end: Point,
            amplitude: float,
            subDivs: int = 7) -> List[Point]:
        """
        Generate points along a circular arc from current endpoint to the given endpoint.
        The amplitude is a number between -1 and 1. 1 means that the center of the circle is
        directly between the start and the endpoint, which creates a full semi circle. 0 creates
        a flat line, and -1 creates the mirror image of the one created with 1.

        Args:
            end (Point): New endpoint of the curve
            amplitude (float): Curvature of the arc
            subDivs (int, optional): Number of points between the start and the end. Defaults to 7.

        Returns:
            List[Point]: Points along the arc
        """

        if amplitude == 0:
            return self.line(end, subDivs)
        curvature = clamp(amplitude, -1, 1)

        result: List[Point] = []

        gspace = geoSpaceBetween(self.end, end)
        if curvature < 0:
            curvature = -curvature
            gspace.scaleYBy(-1)

        pivotY = tan(2 * atan(1 / curvature) - pi / 2)
        pivot = Point(0, -pivotY)
        omega = 2 * (pi - 2 * atan(1 / curvature))
        for i in range(subDivs):
            p = (i + 1) / (subDivs + 1)
            phi = (1 - p) * omega

            subDivPoint = Point(1, 0).rotated(pivot, phi)
            gspace.transform(subDivPoint)
            result.append(subDivPoint)

        result.append(deepcopy(end))
        return result

    def reshape(self, geoSpace: GeoSpace) -> None:
        """
        Transform all points of this curve into given geospace

        Args:
            geoSpace (GeoSpace): Geospace to tranform the points into
        """
        for point in self.points:
            geoSpace.transform(point)


    def length(self) -> float:
        result = 0
        for i in range(len(self.points) - 1):
            result += self.points[i].distanceTo(self.points[i + 1])
        if self.closed:
            result += self.points[-1].distanceTo(self.points[0])
        return result


def geoSpaceBetween(p0: Point, p1: Point) -> GeoSpace:
    """
    Create a geospace between two points

    Args:
        p0 (Point): First point
        p1 (Point): Second point

    Returns:
        GeoSpace: Geospace between the points
    """
    scale = p0.distanceTo(p1) / 2
    angle_ = p0.angleTo(p1)
    midpoint = gradient(p0, p1, 0.5)
    return GeoSpace(angle_, scale, scale, midpoint)
