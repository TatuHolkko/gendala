import random
from math import pi
from typing import List
from common.settings import Settings
from common.utility import clamp, gradient
from geometry.point import Point
from geometry.utility import avgPoint
from hierarchy.curve import GeometryException
from hierarchy.ribbon import Ribbon
from generation.curve import CurveGenerator
from generation.pattern import centerLine, randomLinePattern
from generation.utility import check


class RibbonGenerator:

    def __init__(self, settings: Settings) -> None:
        self.curveGenerator = CurveGenerator(settings=settings)

        self.fillScoreAreaCoeff = settings.getItem(
            "Ribbons",
            "fillScoreAreaCoeff",
            float)

        self.fillScoreCentricCoeff = settings.getItem(
            "Ribbons",
            "fillScoreCentricCoeff",
            float)

        self.fillScoreThreshold = settings.getItem(
            "Ribbons",
            "fillScoreThreshold",
            float)

        self.maxWidth = settings.getItem(
            "Ribbons",
            "maxWidth",
            float)
        
        self.collapseWidth = settings.getItem(
            "Ribbons",
            "collapseWidth",
            float)

        self.maxTaperLength = settings.getItem(
            "Ribbons",
            "maxTaperLength",
            float)
        
        self.minTaperLength = settings.getItem(
            "Ribbons",
            "minTaperLength",
            float)
        
        self.pClosed = settings.getItem(
            "Ribbons",
            "P_closed",
            float)

    def fillScore(self, ribbon: Ribbon) -> float:
        """
        Return a score describing how well a ribbon fills area
        and how centric is it's position.

        Args:
            ribbon (Ribbon): Ribbon to evaluate

        Returns:
            float: Fill score
        """
        pattern = ribbon.getPattern()
        midpointsWeighted: List[(Point, float)] = []
        endpoints: List[Point] = []
        for line in pattern.lines:
            midpointsWeighted.append(
                (gradient(
                    line.p0, line.p1, 0.5), line.p0.distanceTo(
                    line.p1)))
            endpoints.append(line.p0)
            endpoints.append(line.p1)
        midpointAvg = avgPoint([mid for mid, _ in midpointsWeighted])
        weightedRadiusSum = sum(
            [midpointAvg.distanceTo(p) * w for p, w in midpointsWeighted])
        weightsSum = sum([w for _, w in midpointsWeighted])
        avgRadius = weightedRadiusSum / weightsSum
        return (4 / pi * avgRadius**2) * self.fillScoreAreaCoeff - \
            abs(midpointAvg.y) * self.fillScoreCentricCoeff

    def getRibbon(
            self,
            start: Point = None,
            end: Point = None) -> Ribbon:
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
            closed = check(self.pClosed) and not (start or end)
            curve = None
            width = random.random() * self.maxWidth
            while(True):
                curve = self.curveGenerator.getCurve(
                    closed=closed, start=start, end=end)
                try:
                    curve.round()
                except GeometryException:
                    continue
                break
            pattern = randomLinePattern()
            n = 1
            taperLength = clamp(random.uniform(self.minTaperLength, self.maxTaperLength), 0, 0.5)
            r = Ribbon(
                curve=curve,
                pattern=pattern,
                closed=closed,
                taperLength=taperLength,
                width=width,
                n=n)
            r.unCollideWidth()
            if r.width < self.collapseWidth:
                r = Ribbon(
                    curve=curve,
                    pattern=centerLine(),
                    closed=closed,
                    taperLength=taperLength,
                    width=0,
                    n=n)
            if self.fillScore(r) > self.fillScoreThreshold:
                break
        return r
