from typing import List
from geospace import GeoSpace


class Riblet:
    """
    Riblet contains a pattern and a geospace.
    """

    def __init__(self, geoSpace: GeoSpace) -> None:
        """
        Initialize

        Args:
            geoSpace (GeoSpace): Coordinate space used to transform the pattern
        """
        self.geoSpace = geoSpace

    def getExtended(self, pattern: List, amount: float) -> List:
        """
        Extend and transform the given pattern into the local coordinate space

        Args:
            pattern (List): List of lines
            amount (float): Y axis scaling of the pattern

        Returns:
            List: List of transformed lines
        """
        result = []
        for line in pattern:
            line[0][1] *= amount
            line[1][1] *= amount
            line[0] = self.geoSpace.getGlobalPos(line[0])
            line[1] = self.geoSpace.getGlobalPos(line[1])
            result.append(line)
        return result
