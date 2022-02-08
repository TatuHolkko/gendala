from math import ceil, pi
import random
from typing import List
from generation.utility import randomCoordinate
from hierarchy.curve import Curve, GeometryException
from hierarchy.pattern import Pattern
from hierarchy.ribbon import Ribbon
from hierarchy.feature import Feature
from hierarchy.layer import Layer
from geometry.point import Point
from geometry.utility import avgPoint
from generation.pattern import centerLine, horizontalLine, randomPattern, verticalLine
from generation.curve import randomCurve
from common.utility import coinFlip, gradient

minWidth = 0.002


class Generator:
    """
    Object for generating random hierarchy structures
    """

    def __init__(self) -> None:
        self.scale = 1

    def fillScore(self, ribbon: Ribbon):
        pattern = ribbon.getPattern()
        midpoints: List[Point] = []
        endpoints: List[Point] = []
        for line in pattern.lines:
            midpoints.append(gradient(line.p0, line.p1, 0.5))
            endpoints.append(line.p0)
            endpoints.append(line.p1)
        midpointAvg = avgPoint(midpoints)
        avgRadius = sum([midpointAvg.distanceTo(p)
                        for p in endpoints]) / len(endpoints)
        return (4 / pi * avgRadius**2) - abs(midpointAvg.y) / 3

    def getLayer(self, radius: float, width: float, repeats: int) -> Layer:

        yEdge = None
        yCenter = None
        if coinFlip():
            yEdge = randomCoordinate()
        if coinFlip():
            yCenter = randomCoordinate()

        f1 = self.getFeature(leftConnection=yEdge, rightConnection=yCenter)
        f2 = self.getFeature(leftConnection=yCenter, rightConnection=yEdge)
        
        pat1 = f1.getPattern()
        
        pat2 = f2.getPattern()
        
        pat2.offsetX(2)
        
        pat1.combine(pat2)
        pat1.offsetX(-1)
        pat1.scaleX(0.5)

        if True:
            pat1.offsetX(-1)
            mirror = Pattern()
            mirror.combine(pat1)
            mirror.scaleX(-1)
            pat1.combine(mirror)
            pat1.scaleX(0.5)

        if coinFlip() or coinFlip():
            pat1.combine(horizontalLine(-1))
    
        l = Layer(radius=radius, width=width, pattern=pat1, repeats=ceil(repeats / 2))
        return l

    def getFeature(self, leftConnection: float = None,
                   rightConnection: float = None) -> Feature:
        """
        Generate a random Feature

        Args:
            leftConnection (float): If given, y coordinate of left connection
            rightConnection (float): If given, y coordinate of right connection

        Returns:
            Feature: A random Feature
        """
        mirrorX = coinFlip()

        if leftConnection and (not rightConnection) and mirrorX:
            rightConnection = leftConnection
        elif rightConnection and (not leftConnection) and mirrorX:
            leftConnection = rightConnection
        elif rightConnection and leftConnection and (not leftConnection == rightConnection):
            mirrorX = False

        mirrorY = coinFlip()

        if mirrorY:
            if leftConnection:
                leftConnection = abs(leftConnection) - 0.5
            if rightConnection:
                rightConnection = abs(rightConnection) - 0.5

        feature = Feature(mirrorY=mirrorY, mirrorX=mirrorX)

        n = 1 # random.choice([1, 1, 2])
        connectedLeft = random.choice(range(n))
        connectedRight = random.choice(range(n))
        for i in range(n):
            start = None
            end = None
            if i == connectedLeft and leftConnection:
                start = Point(-1, leftConnection)
            if i == connectedRight and rightConnection:
                end = Point(1, rightConnection)
            feature.add(self.getRibbon(start=start, end=end))

        return feature

    def getRibbon(self, start: Point = None, end: Point = None) -> Ribbon:
        """
        Generate a random Ribbon

        If start or end are not given, they are random

        Args:
            start (Point): Start of the ribbon
            end (Point): End of the ribbon

        Returns:
            Ribbon: A random Ribbon
        """
        r = None
        while(True):
            closed = coinFlip() and not (start or end)
            curve = None
            width = random.random() * 0.2
            while(True):
                curve = randomCurve(closed=closed, start=start, end=end)
                try:
                    curve.round()
                except GeometryException:
                    print("Invalid Curve discarded.")
                    continue
                break
            pattern = randomPattern()
            n = random.randint(1, 10)
            taperLength = max(0.5, random.random() - 0.5)
            r = Ribbon(
                curve=curve,
                pattern=pattern,
                closed=closed,
                taperLength=taperLength,
                width=width,
                n=n)
            r.unCollideWidth()
            if r.width * self.scale < minWidth:
                r = Ribbon(
                    curve=curve,
                    pattern=centerLine(),
                    closed=closed,
                    taperLength=taperLength,
                    width=0,
                    n=n)
            if self.fillScore(r) > 0.5:
                break
            print("Invalid Ribbon discarded.")
        return r
