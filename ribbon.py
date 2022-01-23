from copy import deepcopy
from math import atan, atan2, hypot, pi
from typing import List, Tuple
from curve import Curve
from geospace import GeoSpace
from riblet import Riblet
from utility import Line, Point, angle, distance, gradientPoint, normalizeLines, offsetLines, repeatLines, scaleLines, shorterDistance, totalLength


class Ribbon:
    """
    Ribbon describes a long continuous pattern defined by a series of points
    """

    def __init__(
            self,
            curve: Curve,
            pattern: List[Line],
            closed: bool,
            n: int = 1) -> None:
        """
        Initialize the Ribbon class

        Args:
            curve (Curve): Curve defining the shape of the ribbon
            pattern (List[Line]): Pattern of the ribbon
            closed (bool): If true, endpoints are connected
            n (int, optional): Number of repeated patterns. Defaults to 1.
        """

        self.riblets:List[Riblet] = []
        self.pattern = deepcopy(pattern)
        normalizeLines(self.pattern)
        self.closed = closed

        points = curve.getPoints()
        
        lines = len(points)
        if not closed:
            lines -= 1
        
        self.length = totalLength(points)

        widthPerPattern = self.length / n
        patternScale = widthPerPattern / 2

        tempPattern = repeatLines(self.pattern, n)
        offsetLines(tempPattern, 1)
        scaleLines(tempPattern, patternScale)

        x0 = 0
        x1 = 0
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
            
            x1 += distance(p2, p3)

            self.riblets.append(
                Riblet(
                    self.createGeoSpace(
                        p1,
                        p2,
                        p3,
                        p4),
                    self.slicePattern(x0, x1, tempPattern)))
            
            x0 = x1

    def slicePattern(self, x0:float, x1:float, pattern:List[Line]) -> List[Line]:
        result:List[Line] = []
        for line in pattern:

            lx0 = line.p0.x
            lx1 = line.p1.x

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
                result.append(deepcopy(line))
                continue

            leftP = Point(0,0)
            rightP = Point(0,0)
            if left == lx0:
                leftP.x = line.p0.x
                leftP.y = line.p0.y
                rightP.x = line.p1.x
                rightP.y = line.p1.y
            else:
                leftP.x = line.p1.x
                leftP.y = line.p1.y
                rightP.x = line.p0.x
                rightP.y = line.p0.y

            if (lx0 <= x0 and lx1 >= x1) or (lx1 <= x0 and lx0 >= x1):
                # both points outside limits but line crosses the area
                underflowPortion = (x0 - left) / (right - left)
                overflowPortion = (right - x1) / (right - left)
                start = gradientPoint(leftP, rightP, underflowPortion)
                end = gradientPoint(rightP, leftP, overflowPortion)
                if lx0 < lx1:
                    result.append(Line(start,end))
                else:
                    result.append(Line(end,start))
                continue

            # one point inside, one point outside

            if left < x0:
                # left point outside, right point inside
                portionInside = (right - x0) / (right - left)
                start = gradientPoint(rightP, leftP, portionInside)
                end = rightP
                if lx0 < lx1:
                    result.append(Line(start,end))
                else:
                    result.append(Line(end,start))
            else:
                # right point outside, left point inside
                portionInside = (x1 - left) / (right - left)
                start = leftP
                end = gradientPoint(leftP, rightP, portionInside)
                if lx0 < lx1:
                    result.append(Line(start,end))
                else:
                    result.append(Line(end,start))

        scale = 2 / (x1 - x0)
        for line in result:
            line.p0.x -= x0
            line.p1.x -= x0
            line.p0.x *= scale
            line.p1.x *= scale
            line.p0.x -= 1
            line.p1.x -= 1

        return result

    def createGeoSpace(
            self,
            p1: Point,
            p2: Point,
            p3: Point,
            p4: Point) -> GeoSpace:
        """
        Create a geospace for line p2-p3. If p1 or p4 is not None, they define the
        respective guide angles at ends of the line p2-p3.

        Args:
            p1 (Point): Point before the line
            p2 (Point): Start of the line
            p3 (Point): End of the line
            p4 (Point): Next point after the line

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

    def getLines(self, width:float) -> List[Line]:
        result:List[Line] = []
        for riblet in self.riblets:
            result.extend(riblet.getExtended(width))
        return result
