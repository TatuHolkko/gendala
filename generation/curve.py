import random
from common.settings import Settings
from generation.utility import randomPoint
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
        pass

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

        n = random.choice([3, 3, 3, 4])

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
            # if all random points landed on top of each other
            print("Invalid Curve discarded.")
            return self.randomCurve(closed=closed, start=start, end=end)
        return curve

    def extend(self, curve: Curve, point: Point) -> None:
        """
        Extend the given curve to the given point using a random
        curve function.

        Args:
            curve (Curve): Curve to extend
            point (Point): New endpoint
        """
        subDivs = random.randint(3, 9)
        curveType = random.choice(["sine", "arc", "line"])
        if curveType == "sine":
            curve.extend(
                curve.sine(
                    point,
                    subDivs=subDivs,
                    amplitude=random.random() -
                    0.5))
        elif curveType == "arc":
            curve.extend(
                curve.arc(
                    point,
                    subDivs=subDivs,
                    amplitude=random.random() *
                    2 -
                    1))
        else:
            curve.extend(curve.line(point))

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
