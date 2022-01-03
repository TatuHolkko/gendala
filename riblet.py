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
            x0, y0 =  line[0]
            x1, y1 =  line[1]
            y0 *= amount
            y1 *= amount
            x0, y0 = self.geoSpace.getGlobalPos((x0,y0))
            x1, y1 = self.geoSpace.getGlobalPos((x1,y1))
            result.append([[x0,y0],[x1,y1]])
        return result
