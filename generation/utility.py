import random
from typing import List
from geometry.point import Point

"""
Generally useful functions used in random generation
"""

edgePadding = 0.1


def coinFlip() -> bool:
    """
    Return True or False, both as likely.

    Returns:
        bool: Result
    """
    return random.choice([True, False])


def check(p: float) -> bool:
    """
    Return true with probability p

    Args:
        p (float): Probability between 0 and 1

    Returns:
        bool: true with probability p
    """
    return random.random() < p


def sampleFromDistribution(distribution: List[float]) -> int:
    """
    Return random result from a distribution

    Args:
        distribution (List[float]): Discrete distribution weights

    Returns:
        int: Result from distribution
    """
    choices = range(1, len(distribution) + 1)
    return random.choices(population=choices, weights=distribution, k=1)[0]


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
