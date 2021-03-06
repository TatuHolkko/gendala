from __future__ import annotations
from typing import List
from geometry.point import Point
from geometry.line import Line
from copy import deepcopy


class Pattern:
    """
    Pattern is a collection of lines
    """

    def __init__(self) -> None:
        """
        Initialize the pattern
        """
        self.lines: List[Line] = []
        self.xMin = 0
        self.xMax = 0
        self.yMin = 0
        self.yMax = 0

    def add(self, line: Line) -> None:
        """
        Add a Line into this pattern.

        Args:
            line (Line): Line to add
        """
        self.lines.append(deepcopy(line))
        self.updateLimits(line.p0)
        self.updateLimits(line.p1)

    def combine(self, other: Pattern) -> None:
        """
        Copy all lines from another pattern to this one

        Args:
            other (Pattern): Other pattern to combine into this
        """
        for line in other.lines:
            self.add(deepcopy(line))

    def updateLimits(self, point: Point = None) -> None:
        """
        Update x and y ranges.

        If no new point is given, use all points.

        Args:
            point (Point, optional): New point to use. Defaults to None.
        """
        if point is None:
            self.xMax = 0
            self.xMin = 0
            self.yMax = 0
            self.yMin = 0
            for line in self.lines:
                self.updateLimits(line.p0)
                self.updateLimits(line.p1)
        else:
            self.xMax = max(self.xMax, point.x)
            self.xMin = min(self.xMin, point.x)
            self.yMax = max(self.yMax, point.y)
            self.yMin = min(self.yMin, point.y)

    def getWidth(self) -> float:
        """
        Return the width of the pattern along the x axis.

        Returns:
            float: Width of the pattern
        """
        self.updateLimits()
        return self.xMax - self.xMin

    def normalizeX(self) -> None:
        """
        Scale the pattern along x axis so that its width is 2.
        """
        width = self.getWidth()
        middle = (self.xMax + self.xMin) / 2
        scale = 2 / width
        self.offsetX(-middle)
        self.scaleX(scale)

    def scaleYToLimits(self) -> None:
        """
        Scale y so that the pattern fits the unit square.

        If the pattern y limits fit the unit square, no scaling
        is applied.
        """
        self.updateLimits()
        maxY = max(1, max(abs(self.yMin), abs(self.yMax)))
        if maxY > 1:
            self.scaleY(1 / maxY)

    def offsetX(self, deltaX: float) -> None:
        """
        Offset the x coordinate of all lines by an amount.

        Args:
            deltaX (float): Amount to offset
        """
        for l in self.lines:
            l.p0.x += deltaX
            l.p1.x += deltaX

    def offsetY(self, deltaY: float) -> None:
        """
        Offset the y coordinate of all lines by an amount.

        Args:
            deltaX (float): Amount to offset
        """
        for l in self.lines:
            l.p0.y += deltaY
            l.p1.y += deltaY

    def scaleX(self, scaleX: float) -> None:
        """
        Scale the x coordinate of all lines by an amount.

        Args:
            scaleX (float): Amount to scale
        """
        for l in self.lines:
            l.p0.x *= scaleX
            l.p1.x *= scaleX

    def scaleY(self, scaleY: float) -> None:
        """
        Scale the y coordinate of all lines by an amount.

        Args:
            scaleX (float): Amount to scale
        """
        for l in self.lines:
            l.p0.y *= scaleY
            l.p1.y *= scaleY

    def repeat(self, n: int) -> None:
        """
        Add copies of this pattern next to this pattern.
        Each copy will appear in the positive x direction
        with an offset of 2.

        Args:
            n (int): Number of copies
        """
        width = 2
        newSet = Pattern()
        for i in range(n - 1):
            offset = width * (i + 1)
            for line in self.lines:
                newLine = deepcopy(line)
                newLine.p0.x += offset
                newLine.p1.x += offset
                newSet.add(newLine)
        for newLine in newSet.lines:
            self.add(newLine)

    def __repr__(self) -> str:
        return self.lines.__repr__()
