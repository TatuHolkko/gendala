from typing import List
from geospace import GeoSpace, applyGeospace
from ribbon import Ribbon
from utility import Line, Point


class Feature:

    def __init__(self, mirrorX:bool=False, mirrorY:bool=False) -> None:
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
            bottom = GeoSpace(yScale=0.5, origin=Point(0, -0.5))
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
        self.ribbons.append(ribbon)

    def getLines(self, ext:float) -> List[Line]:
        result:List[Line] = []
        for ribbon in self.ribbons:
            for gspace in self.geoSpaces:
                result.extend(applyGeospace(ribbon.getLines(ext), gspace))
        return result