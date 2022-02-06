from math import pi
import random
from typing import List
from hierarchy.curve import Curve, GeometryException
from hierarchy.ribbon import Ribbon
from hierarchy.feature import Feature
from geometry.point import Point
from geometry.utility import avgPoint
from generation.pattern import centerLine, randomPattern
from generation.curve import randomCurve
from common.utility import coinFlip, gradient


class Generator:
    """
    Object for generating random hierarchy structures
    """

    def __init__(self) -> None:
        pass

    def fillScore(self, ribbon:Ribbon):
        pattern = ribbon.getPattern()
        midpoints:List[Point] = []
        endpoints:List[Point] = []
        for line in pattern.lines:
            midpoints.append(gradient(line.p0, line.p1, 0.5))
            endpoints.append(line.p0)
            endpoints.append(line.p1)
        midpointAvg = avgPoint(midpoints)
        avgRadius = sum([midpointAvg.distanceTo(p) for p in endpoints]) / len(endpoints)
        return 4 / pi*avgRadius**2
        

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
        r = None
        while(True):
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
            if self.fillScore(r) > 0.5:
                break
        return r
