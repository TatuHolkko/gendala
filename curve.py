
from copy import deepcopy
from math import atan, pi, sin, tan
from typing import List, Tuple
from utility import Line, Point, angle, clamp, distance, gradientPoint, innerAngle, rotatePoint
from geospace import GeoSpace


class Curve():

    def __init__(self, start: Point, closed: bool = False) -> None:
        self.points = [deepcopy(start)]
        self.start = self.points[0]
        self.end = self.points[0]
        self.closed = closed

    def extend(self, points: List[Point]) -> None:
        self.points.extend(points)
        self.end = points[-1]
        if self.end == self.start:
            self.closed = True
            del self.end
            self.end = self.points[-1]

    def getPoints(self):
        return deepcopy(self.points)

    def sharpCorners(self, maxAngle: float) -> List[int]:

        result = []

        if self.closed:
            p1 = self.points[-1]
            p2 = self.points[0]
            p3 = self.points[1]
            angle_ = innerAngle(p1, p2, p3)
            if abs(angle_) <= maxAngle:
                result.append(0)

        for i in range(len(self.points) - 2):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            p3 = self.points[i + 2]
            angle_ = innerAngle(p1, p2, p3)
            if abs(angle_) <= maxAngle:
                result.append(i + 1)

        if self.closed:
            p1 = self.points[-2]
            p2 = self.points[-1]
            p3 = self.points[0]
            angle_ = innerAngle(p1, p2, p3)
            if abs(angle_) <= maxAngle:
                result.append(len(self.points) - 1)

        return result

    def round(self, maxAngle: float = pi - pi / 4) -> None:
        pointsToRound = self.sharpCorners(maxAngle)
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
            pointsToRound = self.sharpCorners(maxAngle)

    def roundPoint(self, i: int) -> Tuple[Point, Point]:
        p1 = self.points[i - 1]
        p2 = self.points[i]
        p3 = self.points[(i + 1) % len(self.points)]
        rounded1 = gradientPoint(p2, p1, 0.3)
        rounded2 = gradientPoint(p2, p3, 0.3)
        return (rounded1, rounded2)

    def sine(self,
             end: Point,
             subDivs: int = 15,
             amplitude: float = 0.2) -> List[Point]:

        result: List[Point] = []
        gspace = geoSpaceBetween(self.end, end)
        for i in range(subDivs):
            p = (i + 1) / (subDivs + 1)
            phi = 2 * pi * p
            x = 2 * p - 1
            subDivPoint = gspace.getGlobalPos(Point(x, sin(phi) * amplitude))
            result.append(subDivPoint)
        result.append(deepcopy(end))
        return result

    def line(self,
             end: Point,
             subDivs: int = 0) -> List[Point]:

        result: List[Point] = []

        for i in range(subDivs):
            p = (i + 1) / (subDivs + 1)
            gradPoint = gradientPoint(self.end, end, p)
            result.append(gradPoint)

        result.append(deepcopy(end))
        return result

    def arc(self,
            end: Point,
            curvature: float,
            subDivs: int = 7) -> List[Point]:

        if curvature == 0:
            return self.line(self.end, end, subDivs)
        curvature = clamp(curvature, -1, 1)

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

            subDivPoint = rotatePoint(Point(1, 0), pivot, phi)
            subDivPoint = gspace.getGlobalPos(subDivPoint)
            result.append(subDivPoint)

        result.append(deepcopy(end))
        return result


def geoSpaceBetween(p0: Point, p1: Point) -> GeoSpace:
    scale = distance(p0, p1) / 2
    angle_ = angle(p0, p1)
    midpoint = gradientPoint(p0, p1, 0.5)
    return GeoSpace(angle_, scale, scale, midpoint)


def pointsToLines(points: List[Point]) -> List[Line]:
    result:List[Line] = []
    for i in range(len(points) - 1):
        result.append(Line(deepcopy(points[i]), deepcopy(points[i + 1])))
    return result
