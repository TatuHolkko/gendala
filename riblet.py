from copy import deepcopy
from typing import List
from display import Display
from geometry import Pattern
from geospace import GeoSpace
from geometry import Line


class Riblet():
    """
    Riblet contains a pattern and a geospace.
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

    def render(self, display:Display, width: float) -> None:
        """
        Render the pattern inside this riblet

        Args:
            display (Display): Display to draw on
            width (float): Y axis scaling of the pattern
        """
        self.geoSpace.setYScale(width)

        display.pushGeoSpace(self.geoSpace)

        for line in self.pattern.lines:
            display.drawLine(line)
        
        display.popGeoSpace()
    
    def getPattern(self, width) -> Pattern:
        self.geoSpace.setYScale(width)
        result = Pattern()
        for line in self.pattern.lines:
            p0 = self.geoSpace.getExternalPos(line.p0)
            p1 = self.geoSpace.getExternalPos(line.p1)
            result.add(Line(p0,p1))
        return result
