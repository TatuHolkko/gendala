
from copy import deepcopy
from math import atan, pi, sin, tan
from os import stat
from utility import angle, clamp, distance, gradientPoint, rotatePoint
from geospace import GeoSpace


class Curve():

    def __init__(self, start: list, closed: bool = False) -> None:
        self.points = [[start[0], start[1]]]
        self.start = self.points[0]
        self.end = self.points[0]
        self.closed = closed

    def extend(self, points: list) -> None:
        self.points.extend(points)
        self.end = points[-1]
        if self.end == self.start:
            self.closed = True
            del self.end
            self.end = self.points[-1]
        self.round()

    def getPoints(self):
        return deepcopy(self.points)
        
    def round(self, maxAngle:float = 20):
        pass

    def sine(self,
             end: list,
             subDivs: int = 15,
             amplitude: float = 0.2) -> list:

        result = []
        gspace = geoSpaceBetween(self.end, end)
        for i in range(subDivs):
            p = (i + 1) / (subDivs + 1)
            phi = 2 * pi * p
            x = 2 * p - 1
            subDivPoint = gspace.getGlobalPos((x, sin(phi) * amplitude))
            result.append([subDivPoint[0], subDivPoint[1]])
        result.append([end[0], end[1]])
        return result

    def line(self,
             end: list,
             subDivs: int = 0) -> list:

        result = []

        for i in range(subDivs):
            p = (i + 1) / (subDivs + 1)
            gradPoint = gradientPoint(self.end, end, p)
            result.append([gradPoint[0], gradPoint[1]])

        result.append([end[0], end[1]])
        return result

    def arc(self,
            end: list,
            curvature: float,
            subDivs: int = 7) -> list:

        if curvature == 0:
            return self.line(self.end, end, subDivs)
        curvature = clamp(curvature, -1, 1)

        result = []

        gspace = geoSpaceBetween(self.end, end)
        if curvature < 0:
            curvature = -curvature
            gspace.scaleYBy(-1)

        pivotY = tan(2 * atan(1 / curvature) - pi / 2)
        pivot = (0, -pivotY)
        omega = 2 * (pi - 2 * atan(1 / curvature))
        for i in range(subDivs):
            p = (i + 1) / (subDivs + 1)
            phi = (1 - p) * omega

            subDivPoint = rotatePoint((1, 0), pivot, phi)
            subDivPoint = gspace.getGlobalPos(subDivPoint)
            result.append([subDivPoint[0], subDivPoint[1]])

        result.append([end[0], end[1]])
        return result


def geoSpaceBetween(p0, p1) -> GeoSpace:
    scale = distance(p0, p1) / 2
    angle_ = angle(p0, p1)
    midpoint = gradientPoint(p0, p1, 0.5)
    return GeoSpace(angle_, scale, scale, midpoint)


def pointsToLines(points: list) -> list:
    result = []
    for i in range(len(points) - 1):
        result.append([[points[i][0], points[i][1]],
                      [points[i + 1][0], points[i + 1][1]]])
    return result
