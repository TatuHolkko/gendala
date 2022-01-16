from math import atan, atan2, hypot, pi
from typing import List, Tuple
from curve import Curve
from geospace import GeoSpace
from riblet import Riblet
from utility import angle, delta, distance, gradient, gradientPoint, shorterDistance


class Ribbon:
    """
    Ribbon describes a long continuous pattern defined by a series of points
    """

    def __init__(
            self,
            curve: Curve,
            pattern: List,
            closed: bool,
            n: int = 0) -> None:
        """
        Initialize the ribbon

        Args:
            points (List): Points defining the shape of the ribbon
            pattern (List): Pattern of the ribbon
            closed (bool): if true, endpoints are connected
        """
        self.riblets = []
        self.pattern = pattern
        points = curve.getPoints()

        lines = len(points)
        if not closed:
            lines -= 1

        for i in range(len(points)):

            if not closed and i == len(points) - 1:
                break

            p1 = None
            p2 = points[i]
            p3 = points[(i + 1) % len(points)]
            p4 = None

            if i > 0 or closed:
                p1 = points[i - 1]
            if i < len(points) - 2 or closed:
                p4 = points[(i + 2) % len(points)]

            nPatterns = n
            if nPatterns == 0 or nPatterns > lines:
                nPatterns = lines

            x0 = -1 + ((i * nPatterns / lines) % 1) * 2
            x1 = -1 + (1 - ((1 - ((i + 1) * nPatterns / lines)) % 1)) * 2

            self.riblets.append(
                Riblet(
                    self.createGeoSpace(
                        p1,
                        p2,
                        p3,
                        p4),
                    self.slicePattern(x0, x1, pattern)))

    def slicePattern(self, x0, x1, pattern):
        result = []
        for line in pattern:

            lx0 = line[0][0]
            lx1 = line[1][0]

            left = min(lx0, lx1)
            right = max(lx0, lx1)

            if (right == x0 and left < right) or (left == x1 and left < right):
                # only one point at the limit
                continue
            if (lx0 < x0 and lx1 < x0) or (lx0 > x1 and lx1 > x1):
                # entire line outside limits
                continue
            if ((lx0 >= x0 and lx1 >= x0) and (lx0 <= x1 and lx1 <= x1)):
                # entire line inside limits
                result.append([[line[0][0], line[0][1]],
                              [line[1][0], line[1][1]]])
                continue

            leftP = [0, 0]
            rightP = [0, 0]
            if left == lx0:
                leftP[0] = line[0][0]
                leftP[1] = line[0][1]
                rightP[0] = line[1][0]
                rightP[1] = line[1][1]
            else:
                leftP[0] = line[1][0]
                leftP[1] = line[1][1]
                rightP[0] = line[0][0]
                rightP[1] = line[0][1]

            if (lx0 <= x0 and lx1 >= x1) or (lx1 <= x0 and lx0 >= x1):
                # both points outside limits but line crosses the area
                underflowPortion = (x0 - left) / (right - left)
                overflowPortion = (right - x1) / (right - left)
                start = gradientPoint(leftP, rightP, underflowPortion)
                end = gradientPoint(rightP, leftP, overflowPortion)
                if lx0 < lx1:
                    result.append([[start[0], start[1]], [end[0], end[1]]])
                else:
                    result.append([[end[0], end[1]], [start[0], start[1]]])
                continue

            # one point inside, one point outside

            if left < x0:
                # left point outside, right point inside
                portionInside = (right - x0) / (right - left)
                start = gradientPoint(rightP, leftP, portionInside)
                end = rightP
                if lx0 < lx1:
                    result.append([[start[0], start[1]], [end[0], end[1]]])
                else:
                    result.append([[end[0], end[1]], [start[0], start[1]]])
            else:
                # right point outside, left point inside
                portionInside = (x1 - left) / (right - left)
                start = leftP
                end = gradientPoint(leftP, rightP, portionInside)
                if lx0 < lx1:
                    result.append([[start[0], start[1]], [end[0], end[1]]])
                else:
                    result.append([[end[0], end[1]], [start[0], start[1]]])

        scale = 2 / (x1 - x0)
        for line in result:
            line[0][0] -= x0
            line[1][0] -= x0
            line[0][0] *= scale
            line[1][0] *= scale
            line[0][0] -= 1
            line[1][0] -= 1

        return result

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
            1,
            midpoint,
            startGuide,
            endGuide)

    def getLines(self):
        result = []
        for riblet in self.riblets:
            result.extend(riblet.getExtended(0.3))
        return result
