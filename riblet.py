from copy import deepcopy
from typing import List
from display import Display
from geospace import GeoSpace
from utility import Line


class Riblet():
    """
    Riblet contains a pattern and a geospace.
    """

    def __init__(self, geoSpace: GeoSpace, pattern: List[Line]) -> None:
        """
        Initialize

        Args:
            geoSpace (GeoSpace): Coordinate space used to transform the pattern
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

        for line in self.pattern:
            display.drawLine(line)
        
        display.popGeoSpace()
    
    def getLines(self, width) -> List[Line]:
        self.geoSpace.setYScale(width)
        result:List[Line] = []
        for line in self.pattern:
            p0 = self.geoSpace.getExternalPos(line.p0)
            p1 = self.geoSpace.getExternalPos(line.p1)
            result.append(Line(p0,p1))
        return result
