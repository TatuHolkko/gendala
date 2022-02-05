from __future__ import annotations
from geometry.point import Point
from geometry.line import Line
from copy import deepcopy


class Pattern:
    def __init__(self) -> None:
        self.lines: set[Line] = set()
        self.xMin = 0
        self.xMax = 0
        self.yMin = 0
        self.yMax = 0

    def add(self, line: Line) -> None:
        self.lines.add(deepcopy(line))
        self.updateLimits(line.p0)
        self.updateLimits(line.p1)

    def combine(self, other: Pattern) -> None:
        for line in other.lines:
            self.add(line)

    def updateLimits(self, point: Point = None) -> None:

        if point is None:
            self.xMax = 0
            self.xMin = 0
            self.yMax = 0
            self.yMin = 0
            for line in self.lines:
                self.updateLimits(line.p0)
                self.updateLimits(line.p1)

        self.xMax = max(self.xMax, point.x)
        self.xMin = min(self.xMin, point.x)
        self.yMax = max(self.yMax, point.y)
        self.yMin = min(self.yMin, point.y)

    def getWidth(self) -> float:
        self.updateLimits()
        return self.xMax - self.xMin

    def normalizeX(self) -> None:
        width = self.getWidth()
        middle = (self.xMax + self.xMin) / 2
        scale = 2 / width
        self.offsetX(-middle)
        self.scaleX(scale)

    def offsetX(self, deltaX: float) -> None:
        for l in self.lines:
            l.p0.x += deltaX
            l.p1.x += deltaX

    def scaleX(self, scaleX: float) -> None:
        for l in self.lines:
            l.p0.x *= scaleX
            l.p1.x *= scaleX

    def repeat(self, n: int) -> None:
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
