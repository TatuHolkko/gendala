
from math import atan, pi, sin, tan
from utility import angle, clamp, distance, gradientPoint, rotatePoint
from geospace import GeoSpace


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


def line(
        p0: list,
        p1: list,
        subDivs: int = 0) -> list:

    result = [[p0[0], p0[1]]]

    for i in range(subDivs):
        p = (i + 1) / (subDivs + 1)
        gradPoint = gradientPoint(p0, p1, p)
        result.append([gradPoint[0], gradPoint[1]])

    result.append([p1[0], p1[1]])
    return result


def arc(p0: list,
        p1: list,
        curvature: float,
        subDivs: int = 8) -> list:

    if curvature == 0:
        return line(p0, p1, subDivs)
    curvature = clamp(curvature, -1, 1)

    result = [[p0[0], p0[1]]]

    gspace = geoSpaceBetween(p0, p1)
    if curvature < 0:
        curvature = -curvature
        gspace.scaleYBy(-1)

    pivotY = tan(2 * atan(1 / curvature) - pi / 2)
    pivot = (0, -pivotY)
    omega = 2 * (pi - 2 * atan(1 / curvature))
    for i in range(subDivs):
        p = (i + 1) / (subDivs + 1)
        phi = (1-p) * omega

        subDivPoint = rotatePoint((1,0), pivot, phi)
        subDivPoint = gspace.getGlobalPos(subDivPoint)
        result.append([subDivPoint[0], subDivPoint[1]])

    result.append([p1[0], p1[1]])
    return result
