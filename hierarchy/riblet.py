from system.display import Display
from geometry.point import Point
from geometry.line import Line
from geometry.geospace import GeoSpace
from hierarchy.pattern import Pattern


class Riblet():
    """
    Riblet is a piece of Ribbon that contains a Pattern and a GeoSpace.
    """

    def __init__(self, geoSpace: GeoSpace, pattern: Pattern) -> None:
        """
        Initialize

        Args:
            geoSpace (GeoSpace): Coordinate space used to transform the pattern
            pattern (Pattern): Pattern to draw
        """
        self.geoSpace = geoSpace
        self.pattern = pattern

    def render(self, display: Display) -> None:
        """
        Render the pattern inside this riblet

        Args:
            display (Display): Display to draw on
        """

        display.pushGeoSpace(self.geoSpace)

        for line in self.pattern.lines:
            display.drawLine(line)

        display.popGeoSpace()

    def collisionHeight(self) -> float:
        """
        Calculate the y coordinate at which the start and end angles
        cause a collision of points at x=1 and x=-1. If collision is
        very far away, return 0.

        Returns:
            float: y coordinate
        """
        deltaY = 0.01
        deltaThreshold = 0.001
        tempGS = GeoSpace(
            startAngle=self.geoSpace.startAngle,
            endAngle=self.geoSpace.endAngle)
        p1 = tempGS.getExternalPos(Point(-1, 0))
        p2 = tempGS.getExternalPos(Point(1, 0))
        d0 = p1.distanceTo(p2)
        p1 = tempGS.getExternalPos(Point(-1, deltaY))
        p2 = tempGS.getExternalPos(Point(1, deltaY))
        d1 = p1.distanceTo(p2)
        dd = d1 - d0
        if abs(dd) < deltaThreshold:
            return 0
        return d0 / dd * deltaY * self.geoSpace.scale[0]

    def getPattern(self) -> Pattern:
        """
        Create a pattern from this Riblet

        Returns:
            Pattern: Pattern from this Riblet
        """
        result = Pattern()
        for line in self.pattern.lines:
            p0 = self.geoSpace.getExternalPos(line.p0)
            p1 = self.geoSpace.getExternalPos(line.p1)
            result.add(Line(p0, p1))
        return result
