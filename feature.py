from typing import List
from display import Display
from geospace import GeoSpace
from ribbon import Ribbon
from geometry import Line, Pattern, Point


class Feature:
    """
    Feature contains several ribbons and mirroring options
    """

    def __init__(self, mirrorX:bool=False, mirrorY:bool=False) -> None:
        """
        Initialize the class

        Args:
            mirrorX (bool, optional): Mirror along x axis. Defaults to False.
            mirrorY (bool, optional): Mirror along y axis. Defaults to False.
        """
        self.ribbons:List[Ribbon] = []
        self.mirrorX = mirrorX
        self.mirrorY = mirrorY
        self.geoSpaces:List[GeoSpace] = []
        if mirrorX and not mirrorY:
            left = GeoSpace(xScale=-0.5, origin=Point(-0.5, 0))
            right = GeoSpace(xScale=0.5, origin=Point(0.5, 0))
            self.geoSpaces.append(left)
            self.geoSpaces.append(right)
        elif mirrorY and not mirrorX:
            top = GeoSpace(yScale=0.5, origin=Point(0, 0.5))
            bottom = GeoSpace(yScale=-0.5, origin=Point(0, -0.5))
            self.geoSpaces.append(top)
            self.geoSpaces.append(bottom)
        elif mirrorX and mirrorY:
            northEast = GeoSpace(yScale=0.5, xScale=0.5, origin=Point(0.5, 0.5))
            southEast = GeoSpace(yScale=-0.5, xScale=0.5, origin=Point(0.5, -0.5))
            southWest = GeoSpace(yScale=-0.5, xScale=-0.5, origin=Point(-0.5, -0.5))
            northWest = GeoSpace(yScale=0.5, xScale=-0.5, origin=Point(-0.5, 0.5))
            self.geoSpaces.append(northEast)
            self.geoSpaces.append(southEast)
            self.geoSpaces.append(southWest)
            self.geoSpaces.append(northWest)
        else:
            self.geoSpaces.append(GeoSpace())

    def add(self, ribbon:Ribbon) -> None:
        """
        Add a ribbon to this feature

        Args:
            ribbon (Ribbon): Ribbon to add
        """
        for geospace in self.geoSpaces:
            self.ribbons.append(ribbon.reshaped(geospace))

    def render(self, display:Display) -> None:
        """
        Render lines created by this feature

        Args:
            display (Display): Display to draw on
        """
        for ribbon in self.ribbons:
            ribbon.render(display)
    
    def getPattern(self) -> Pattern:
        result = Pattern()
        for ribbon in self.ribbons:
            for line in ribbon.getPattern().lines:
                result.add(line)
        return result