import random
from common.settings import Settings
from generation.utility import sampleFromDistribution, randomPoint
from hierarchy.curve import Curve
from geometry.point import Point
from typing import List


class CurveGenerator:
    """
    Generator for Curve objects
    """

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the generator

        Args:
            settings (Settings): Settings object
        """
        self.pdNPoints = settings.getList(
            section="Curves",
            setting="PD_complexity",
            constructor=float
        )
        self.pdSubDivs = settings.getList(
            section="Curves",
            setting="PD_subDivisions",
            constructor=float
        )
        self.pdExtensionType = settings.getList(
            section="Curves",
            setting="PD_connectionType",
            constructor=float
        )
        self.maxAmpSine = settings.getItem(
            section="Curves",
            setting="maxSineAmplitude",
            constructor=float
        )
        self.maxAmpArc = settings.getItem(
            section="Curves",
            setting="maxArcAmplitude",
            constructor=float
        )

    def getCurve(
            self,
            closed=False,
            start: Point = None,
            end: Point = None) -> Curve:
        """
        Generate a random Curve

        If start or end are not given, they are random

        Args:
            closed (bool, optional): Wether to close the curve. Defaults to False.
            start (Point): Start of the ribbon
            end (Point): End of the ribbon

        Returns:
            Curve: A random Curve
        """

        points: List[Point] = []

        n = 2 + sampleFromDistribution(self.pdNPoints)

        if start:
            points.append(start)
            n -= 1
        if end:
            n -= 1

        points.extend(self.getPoints(n))

        if end:
            points.append(end)

        curve = Curve(points[0], closed=closed)
        for point in points[1:]:
            self.extend(curve, point)
        curve.removeDuplicates()
        if (len(curve.points) < 2) or (len(curve.points) < 3 and closed):
            print("\t\t\t\tPoint locations invalid, discarded.")
            return self.getCurve(closed=closed, start=start, end=end)
        return curve

    def extend(self, curve: Curve, point: Point) -> None:
        """
        Extend the given curve to the given point using a random
        curve function.

        Args:
            curve (Curve): Curve to extend
            point (Point): New endpoint
        """
        subDivs = sampleFromDistribution(self.pdSubDivs)
        curveType = sampleFromDistribution(self.pdExtensionType)
        if curveType == 3:
            curve.extend(
                curve.sine(
                    point,
                    subDivs=subDivs,
                    amplitude=random.random() * self.maxAmpSine))
        elif curveType == 2:
            curve.extend(
                curve.arc(
                    point,
                    subDivs=subDivs,
                    amplitude=random.random() * self.maxAmpArc))
        elif curveType == 1:
            curve.extend(curve.line(point))
        else:
            raise ValueError("Invalid curve type id")

    @staticmethod
    def getPoints(n: int = 2) -> List[Point]:
        """
        Generate a random set of points

        Args:
            n (int): Number of points

        Returns:
            List[Point]: A random set of points
        """
        points = []

        for _ in range(n):
            points.append(randomPoint())

        return points
