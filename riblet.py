from copy import deepcopy
from typing import List
from geospace import GeoSpace
from utility import Line


class Riblet:
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

    def getExtended(self, amount: float) -> List[Line]:
        """
        Extend and transform the given pattern into the local coordinate space

        Args:
            pattern (List): List of lines
            amount (float): Y axis scaling of the pattern

        Returns:
            List: List of transformed lines
        """

        result:List[Line] = []
        for line in self.pattern:
            p0 =  deepcopy(line.p0)
            p1 =  deepcopy(line.p1)
            p0.y *= amount
            p1.y *= amount
            p0 = self.geoSpace.getGlobalPos(p0)
            p1 = self.geoSpace.getGlobalPos(p1)
            result.append(Line(p0,p1))
        return result
