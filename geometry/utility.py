from geometry.point import Point
from math import pi

Angle = float

def deg(a: Angle) -> float:
    """
    Convert radians to degrees

    Args:
        a (Angle): Angle in radians

    Returns:
        float: Angle in degrees
    """
    return a * 180 / pi


def wrap(a: Angle) -> Angle:
    """
    Wrap angle between pi and -pi

    Args:
        value (float): Angle to wrap

    Returns:
        float: Angle between pi and -pi
    """
    return (a + pi) % (2 * pi) - pi


def convexAngle(a1: Angle, a2: Angle) -> Angle:
    """
    Return the smaller angle between the given angles.
    This function solves the problem where the angles have different signs
    so the subtraction results in an angle above pi.

    Args:
        a1 (Angle): First angle
        a2 (Angle): Second angle

    Returns:
        Angle: Angle a2-a1, chosen on the side that is below pi
    """
    angle1 = wrap(a1)
    angle2 = wrap(a2)
    dist = abs(angle2 - angle1)

    if dist > pi:
        dist = 2 * pi - abs(angle1) - abs(angle2)
        if angle1 > angle2:
            return dist
        return -dist

    return angle2 - angle1


def cornerAngle(p1: Point, corner: Point, p2: Point) -> Angle:
    """
    Return the sharp angle at corner

    The angle is the inner angle at "corner" in a triangle p1-corner-p3

    Args:
        p1 (Point): First connection point
        corner (Point): Corner point at which the angle is measured
        p2 (Point): Second connection point

    Returns:
        Angle: Sharp angle at the corner
    """
    return convexAngle(corner.angleTo(p1), corner.angleTo(p2))
