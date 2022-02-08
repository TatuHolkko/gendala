import random
from geometry.point import Point

edgePadding = 0.1

def randomCoordinate() -> float:
    """
    Return a random coordinate between -1 and 1

    Returns:
        float: The coordinate
    """
    return (random.random() * 2 - 1) * (1 - edgePadding)

def randomPoint() -> Point:
    """
    Return a random point inside the unit square.

    Returns:
        Point: Point inside the unit square
    """
    return Point(randomCoordinate(), randomCoordinate())

