import random
from geometry.point import Point
from hierarchy.curve import Curve
from hierarchy.pattern import Pattern

"""
Collection of patterns
"""

def verticalLine(x=0) -> Pattern:
    pattern = Pattern()
    line = Curve(Point(x, 1))
    line.extend(line.line(Point(x, -1)))
    pattern.combine(line.getPattern())
    return pattern


def horizontalLine(y=0) -> Pattern:
    pattern = Pattern()
    line = Curve(Point(-1, y))
    line.extend(line.line(Point(1, y)))
    pattern.combine(line.getPattern())
    return pattern


def diagonal(flipped=True) -> Pattern:
    pattern = Pattern()
    line = Curve(Point(1, 1))
    line.extend(line.line(Point(-1, -1)))
    pattern.combine(line.getPattern())
    if flipped:
        pattern.scaleX(-1)
    return pattern


def leftAndRight() -> Pattern:
    pattern = Pattern()
    pattern.combine(verticalLine(1))
    pattern.combine(verticalLine(-1))
    return pattern


def topAndBottom() -> Pattern:
    pattern = Pattern()
    pattern.combine(horizontalLine(1))
    pattern.combine(horizontalLine(-1))
    return pattern


def box() -> Pattern:
    pattern = Pattern()
    pattern.combine(topAndBottom())
    pattern.combine(leftAndRight())
    return pattern


def crossedBox() -> Pattern:
    pattern = Pattern()
    pattern.combine(box())
    pattern.combine(diagonal(flipped=False))
    pattern.combine(diagonal(flipped=True))
    return pattern


def centerLine() -> Pattern:
    pattern = Pattern()
    pattern.combine(horizontalLine(0))
    return pattern


def tripleLine() -> Pattern:
    pattern = Pattern()
    pattern.combine(topAndBottom())
    pattern.combine(horizontalLine(0))
    return pattern


def zed() -> Pattern:
    pattern = Pattern()
    pattern.combine(topAndBottom())
    pattern.combine(diagonal())
    return pattern


def ladder() -> Pattern:
    pattern = Pattern()
    pattern.combine(topAndBottom())
    pattern.combine(verticalLine(0))
    return pattern


def rope() -> Pattern:
    pattern = Pattern()
    pattern.combine(topAndBottom())
    line = Curve(Point(1, 1))
    line.extend(line.line(Point(-1, -1)))
    pattern.combine(line.getPattern())
    line = Curve(Point(0, 1))
    line.extend(line.line(Point(-1, 0)))
    pattern.combine(line.getPattern())
    line = Curve(Point(1, 0))
    line.extend(line.line(Point(0, -1)))
    pattern.combine(line.getPattern())
    return pattern

def arrows() -> Pattern:
    pattern = Pattern()
    pattern.combine(topAndBottom())
    line = Curve(Point(1, 1))
    line.extend(line.line(Point(0, 0)))
    pattern.combine(line.getPattern())
    line = Curve(Point(1, -1))
    line.extend(line.line(Point(0, 0)))
    pattern.combine(line.getPattern())
    return pattern

def spikes() -> Pattern:
    pattern = Pattern()
    pattern.combine(horizontalLine(y=-1))
    line = Curve(Point(0, 1))
    line.extend(line.line(Point(-1, -1)))
    pattern.combine(line.getPattern())
    line = Curve(Point(0, 1))
    line.extend(line.line(Point(1, -1)))
    pattern.combine(line.getPattern())
    return pattern

def crissCross() -> Pattern:
    pattern = Pattern()
    pattern.combine(topAndBottom())
    pattern.combine(diagonal(flipped=False))
    pattern.combine(diagonal(flipped=True))
    return pattern

def randomComplexPattern() -> Pattern:
    func = random.choice([topAndBottom,
                          crissCross,
                          spikes,
                          arrows,
                          ladder])
    return func()

def randomLinePattern() -> Pattern:
    func = random.choice([tripleLine,
                          topAndBottom,
                          centerLine])
    return func()
