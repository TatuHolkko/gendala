from __future__ import annotations
from copy import deepcopy
from math import floor
from typing import List
from common.utility import clamp, gradient
from geometry.utility import convexAngle
from geometry.point import Point
from geometry.line import Line
from geometry.geospace import GeoSpace
from hierarchy.pattern import Pattern
from hierarchy.curve import Curve
from hierarchy.riblet import Riblet
from system.display import Display


class Ribbon():
    """
    Ribbon describes a long continuous pattern defined by a series of points
    """

    def __init__(
            self,
            curve: Curve,
            pattern: Pattern,
            closed: bool,
            width: float,
            taperLength: float = 0,
            n: int = 1) -> None:
        """
        Initialize the Ribbon class

        Args:
            curve (Curve): Curve defining the shape of the ribbon
            pattern (Pattern): Pattern of the ribbon
            closed (bool): If true, endpoints are connected
            width (float): Width of the ribbon
            taperLength (float): Percentage of line length used in both ends for tapering
            n (int, optional): Number of repeated patterns. Defaults to 1.
        """

        self.curve = curve
        self.pattern = pattern
        self.closed = closed
        self.width = width
        self.taperLength = taperLength
        self.n = n

        self.riblets: List[Riblet] = []

        points = curve.getPoints()
        self.taperLengthIndex = floor(taperLength * (len(points) - 1))

        lines = len(points)
        if not closed:
            lines -= 1

        self.length = self.curve.length()

        widthPerPattern = self.length / n
        patternScale = widthPerPattern / 2

        tempPattern = deepcopy(self.pattern)
        tempPattern.repeat(n + 2)
        tempPattern.offsetX(-1)
        tempPattern.scaleX(patternScale)

        x0 = 0
        x1 = 0

        for i in range(len(points)):

            if not closed and i == len(points) - 1:
                break

            p1 = None
            p2 = points[i]
            p3 = points[(i + 1) % len(points)]
            p4 = None

            startTaper = self.taperScale(i)
            endTaper = self.taperScale(i + 1)

            if i > 0 or closed:
                p1 = points[i - 1]
            if i < len(points) - 2 or closed:
                p4 = points[(i + 2) % len(points)]

            x1 += p2.distanceTo(p3)

            self.riblets.append(
                Riblet(
                    self.createGeoSpace(
                        p1=p1,
                        p2=p2,
                        p3=p3,
                        p4=p4,
                        startTaper=startTaper,
                        endTaper=endTaper,
                        yScale=width),
                    self.slicePattern(x0, x1, tempPattern)))

            x0 = x1

    def taperScale(self, index: int) -> float:

        if self.taperLengthIndex < 1 or self.closed:
            return 1

        startTaper = index / self.taperLengthIndex
        inverseIndex = len(self.curve.getPoints()) - index - 1
        endTaper = inverseIndex / self.taperLengthIndex
        startTaper = clamp(startTaper, 0, 1)
        endTaper = clamp(endTaper, 0, 1)
        return min(startTaper, endTaper)

    def __repr__(self) -> str:
        return self.curve.__repr__() + ", closed=" + str(self.closed)

    def reshaped(self, geoSpace: GeoSpace) -> Ribbon:
        """
        Create a copy of this ribbon, with it's curve reshaped in the given geospace

        Args:
            geoSpace (GeoSpace): Geospace to use

        Returns:
            Ribbon: Reshaped copy of this Ribbon
        """
        curve = deepcopy(self.curve)
        curve.reshape(geoSpace)
        xScale, yScale = geoSpace.getScale()
        pattern = deepcopy(self.pattern)
        if xScale * yScale < 0:
            flip = GeoSpace()
            flip.scaleYBy(-1)
            flip.transform(pattern)
        return Ribbon(
            curve=curve,
            pattern=pattern,
            closed=self.closed,
            taperLength=self.taperLength,
            n=self.n,
            width=self.width)

    def slicePattern(
            self,
            x0: float,
            x1: float,
            pattern: Pattern) -> Pattern:
        """
        Return a slice of a given pattern. The slice will be normalized to stretch from
        x=-1 to x=1.

        Args:
            x0 (float): Lower x limit
            x1 (float): Higher x limit
            pattern (Pattern): Pattern to slice

        Returns:
            Pattern: Normalized pattern slice from x0 to x1
        """
        result = Pattern()
        for line in pattern.lines:

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
                result.add(deepcopy(line))
                continue

            leftP = Point(0, 0)
            rightP = Point(0, 0)
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
                start = gradient(leftP, rightP, underflowPortion)
                end = gradient(rightP, leftP, overflowPortion)
                if lx0 < lx1:
                    result.add(Line(start, end))
                else:
                    result.add(Line(end, start))
                continue

            # one point inside, one point outside

            if left < x0:
                # left point outside, right point inside
                portionInside = (right - x0) / (right - left)
                start = gradient(rightP, leftP, portionInside)
                end = rightP
                if lx0 < lx1:
                    result.add(Line(start, end))
                else:
                    result.add(Line(end, start))
            else:
                # right point outside, left point inside
                portionInside = (x1 - left) / (right - left)
                start = leftP
                end = gradient(leftP, rightP, portionInside)
                if lx0 < lx1:
                    result.add(Line(start, end))
                else:
                    result.add(Line(end, start))

        scale = 2 / (x1 - x0)

        result.offsetX(-x0)
        result.scaleX(scale)
        result.offsetX(-1)

        return result

    def createGeoSpace(
            self,
            p1: Point,
            p2: Point,
            p3: Point,
            p4: Point,
            startTaper: float,
            endTaper: float,
            yScale: float) -> GeoSpace:
        """
        Create a geospace for line p2-p3. If p1 or p4 is not None, they define the
        respective guide angles at ends of the line p2-p3.

        Args:
            p1 (Point): Point before the line
            p2 (Point): Start of the line
            p3 (Point): End of the line
            p4 (Point): Next point after the line
            startTaper (float): Taper scaling at p2
            endTaper (float): Taper scaling at p3
            yScale (float): Y scaling of the pattern

        Returns:
            GeoSpace: GeoSpace for line p2-p3
        """
        currentAngle = p2.angleTo(p3)
        previousAngle = currentAngle
        nextAngle = currentAngle

        if p1 is not None:
            previousAngle = p1.angleTo(p2)
        if p4 is not None:
            nextAngle = p3.angleTo(p4)

        startAngle = convexAngle(currentAngle, previousAngle) / 2
        endAngle = convexAngle(currentAngle, nextAngle) / 2

        xScale = p2.distanceTo(p3) / 2

        midpoint = gradient(p2, p3, 0.5)

        return GeoSpace(
            angle=currentAngle,
            xScale=xScale,
            yScale=yScale,
            origin=midpoint,
            startAngle=startAngle,
            endAngle=endAngle,
            startScale=startTaper,
            endScale=endTaper)

    def unCollideWidth(self):
        collisionWidth = self.width
        for riblet in self.riblets:
            collision = riblet.collisionHeight()
            if collision != 0:
                collisionWidth = min(collisionWidth, abs(collision))
        if collisionWidth != self.width:
            for riblet in self.riblets:
                riblet.geoSpace.setYScale(collisionWidth)
            self.width = collisionWidth

    def render(self, display: Display) -> None:
        """
        Render a list of lines created by this ribbon

        Args:
            display (Display): Display to draw on
        """
        for riblet in self.riblets:
            riblet.render(display)

    def getPattern(self) -> Pattern:
        result = Pattern()
        for riblet in self.riblets:
            for line in riblet.getPattern().lines:
                result.add(line)
        return result
