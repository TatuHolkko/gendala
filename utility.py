
from copy import deepcopy
import math


def delta(start, end):
    return (end[0] - start[0], end[1] - start[1])


def clamp(value, minLim, maxLim):
    return min(max(value, minLim), maxLim)


def sign(value):
    return int(value >= 0) * 2 - 1


def piWrap(angle):
    """
    Wrap angle between pi and -pi
    """
    return (angle + math.pi) % (2 * math.pi) - math.pi


def shorterDistance(angle1, angle2):
    """
    Return the shorter angle between wrapped angle1 and wrapped angle2.
    This function solves the problem where the angles have different signs
    so the subtraction results in an angle above pi.

    Args:
        angle1 (float): Angle 1
        angle2 (float): Angle 2

    Returns:
        float: shorter angular distance from angle1 to angle2
    """
    angle1 = piWrap(angle1)
    angle2 = piWrap(angle2)
    dist = abs(angle2 - angle1)

    if dist > math.pi:
        dist = 2 * math.pi - abs(angle1) - abs(angle2)
        if angle1 > angle2:
            return dist
        return -dist

    return angle2 - angle1


def angle(p1, p2):
    d = delta(p1, p2)
    return math.atan2(d[1], d[0])

def innerAngle(p1,p2,p3):
    return shorterDistance(angle(p2,p1),angle(p2,p3))


def xLimits(points):
    resultMin = None
    resultMax = None
    for point in points:
        if resultMin is None or point[0] < resultMin:
            resultMin = point[0]
        if resultMax is None or point[0] > resultMax:
            resultMax = point[0]
    return [resultMin, resultMax]

def distance(p1, p2):
    d = delta(p1, p2)
    return math.hypot(d[0], d[1])

def totalLength(points, closed=False):
        result = 0
        for i in range(len(points) - 1):
            result += distance(points[i], points[i+1])
        if closed:
            result += distance(points[-1], points[0])
        return result

def offsetLines(lines, deltaX):
    for line in lines:
        line[0][0] += deltaX
        line[1][0] += deltaX

def scaleLines(lines, scaleX):
    for line in lines:
        line[0][0] *= scaleX
        line[1][0] *= scaleX


def pointsFromLines(lines):
    result = set()
    for line in lines:
        result.add(tuplify(line[0]))
        result.add(tuplify(line[1]))
    return list(result)

def normalizeLines(lines):
    xMin, xMax = xLimits(pointsFromLines(lines))
    width = xMax - xMin
    middle = (xMax + xMin) / 2
    scale = 2 / width
    offsetLines(lines, -middle)
    scaleLines(lines, scale)


def repeatLines(lines, n):
    xMin, xMax = xLimits(pointsFromLines(lines))
    width = xMax - xMin
    result = set()
    for i in range(n):
        offset = width * i
        tempLines = deepcopy(lines)
        offsetLines(tempLines, offset)
        for line in tempLines:
            result.add(tuplify(line))
    return listify(result)

def applyGeospace(lines, geospace):
    result = []
    for line in lines:
        x1, y1 = geospace.getGlobalPos(line[0])
        x2, y2 = geospace.getGlobalPos(line[1])
        result.append([[x1,y1],[x2,y2]])
    return result
    


def tuplify(lst):
    # convert list to tuple
    return tuple(tuplify(i) if isinstance(i, list) else i for i in lst)

def listify(tpl):
    # convert tuple to list
    return list(listify(i) if isinstance(i, tuple) else i for i in tpl)


def gradientPoint(p1, p2, s):
    d = delta(p1, p2)
    return (p1[0] + d[0] * s, p1[1] + d[1] * s)


def gradient(v1, v2, s):
    d = v2 - v1
    return v1 + d * s

def rotatePoint(point, pivot, theta):
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
