import random
from hierarchy.curve import Curve, GeometryException
from hierarchy.ribbon import Ribbon
from hierarchy.feature import Feature
from geometry.point import Point
from generation.pattern import centerLine, randomPattern
from generation.curve import randomCurve
from common.utility import coinFlip


class Generator:
    """
    Object for generating random hierarchy structures
    """

    def __init__(self) -> None:
        pass

    def getFeature(self) -> Feature:
        """
        Generate a random Feature

        Returns:
            Feature: A random Feature
        """
        feature = Feature(mirrorY=coinFlip(), mirrorX=coinFlip())
        n = random.choice([1, 1, 2])
        for _ in range(n):
            feature.add(self.getRibbon())
        if coinFlip() or coinFlip():
            line = Curve(Point(-1, 1))
            line.extend(line.line(Point(1, 1)))
            feature.add(
                Ribbon(
                    curve=line,
                    pattern=centerLine(),
                    closed=False,
                    width=1))
        return feature

    def getRibbon(self) -> Ribbon:
        """
        Generate a random Ribbon

        Returns:
            Ribbon: A random Ribbon
        """
        closed = coinFlip()
        curve = None
        width = random.random() * 0.2
        while(True):
            curve = randomCurve(closed=closed)
            try:
                curve.round()
            except GeometryException:
                continue
            break
        pattern = randomPattern()
        n = random.randint(1, 10)
        taperLength = max(0, random.random() - 0.5)
        r = Ribbon(
            curve=curve,
            pattern=pattern,
            closed=closed,
            taperLength=taperLength,
            width=width,
            n=n)
        r.unCollideWidth()
        return r
