from math import atan, atan2, hypot, pi
from typing import List, Tuple
from geospace import GeoSpace
from riblet import Riblet
from utility import angle, delta, distance, gradientPoint, shorterDistance


class Ribbon:
    """
    Ribbon describes a long continuous pattern defined by a series of points
    """

    def __init__(self, points: List, pattern: List, closed: bool) -> None:
        """
        Initialize the ribbon

        Args:
            points (List): Points defining the shape of the ribbon
            pattern (List): Pattern of the ribbon
            closed (bool): if true, endpoints are connected
        """
        self.riblets = []
        self.pattern = pattern

        for i in range(len(points)):

            if not closed and i == len(points) - 1:
                break

            p1 = None
            p2 = points[i]
            p3 = points[(i + 1) % len(points)]
            p4 = None

            if i > 0 or closed:
                p1 = points[i - 1]
            if i < len(points) - 1 or closed:
                p4 = points[(i + 2) % len(points)]

            self.riblets.append(Riblet(self.createGeoSpace(p1, p2, p3, p4)))

    def createGeoSpace(
            self,
            p1: float,
            p2: float,
            p3: float,
            p4: float) -> GeoSpace:
        """
        Create a geospace for line p2-p3. If p1 or p4 is not None, they define the 
        respective guide angles at ends of the line p2-p3.

        Args:
            p1 (float): Point before the line
            p2 (float): Start of the line
            p3 (float): End of the line
            p4 (float): Next point after the line

        Returns:
            GeoSpace: GeoSpace for line p2-p3
        """
        currentAngle = angle(p2, p3)
        previousAngle = currentAngle
        nextAngle = currentAngle

        if p1 is not None:
            previousAngle = angle(p1, p2)
        if p4 is not None:
            nextAngle = angle(p3, p4)

        startGuide = shorterDistance(currentAngle, previousAngle) / 2
        endGuide = shorterDistance(currentAngle, nextAngle) / 2

        scale = distance(p2, p3) / 2

        midpoint = gradientPoint(p2, p3, 0.5)

        return GeoSpace(
            currentAngle,
            scale,
            scale,
            midpoint,
            startGuide,
            endGuide)

    def getLines(self):
        result = []
        for riblet in self.riblets:
            result.extend(riblet.getExtended(self.pattern, 0.3))
        return result
