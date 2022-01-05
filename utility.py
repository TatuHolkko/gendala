
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
    d = delta(p1,p2)
    return math.atan2(d[1], d[0])

def distance(p1, p2):
    d = delta(p1, p2)
    return math.hypot(d[0], d[1])

def gradientPoint(p1, p2, s):
    d = delta(p1, p2)
    return (p1[0] + d[0] * s, p1[1] + d[1] * s)

def ext(indexes):

    extension = [
        #hor
        [[-1, 1], [1, 1]],
        [[-1, 0], [1, 0]],
        [[-1, -1], [1, -1]],
        #diag
        [[1,-1],[-1,1]],
        [[-1,-1],[1,1]],
        #ver
        [[-1, 1], [-1, -1]],
        [[0, 1], [0, -1]],
        [[1, 1], [1, -1]],
    ]

    result = []
    for i in indexes:
        result.append(extension[i])

    return result