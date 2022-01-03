from math import atan2, hypot, pi
from typing import List, Tuple
from geospace import GeoSpace
from riblet import Riblet
from utility import delta

class Ribbon:
    """
    Ribbon describes a long continuous pattern defined by a series of points
    """

    def __init__(self, points: List, pattern: List) -> None:
        """
        Initialize the ribbon

        Args:
            points (List): Points defining the shape of the ribbon
            pattern (List): Pattern of the ribbon
        """
        self.riblets = []
        self.pattern = pattern
        anglePrev = 0
        for i in range(len(points) - 1):
            
            start = points[i]
            end = points[i + 1]
            
            deltaCurrent = delta(start, end)
            
            angleCurrent = atan2(deltaCurrent[1], deltaCurrent[0])

            angleNext = angleCurrent
            if (i < len(points) - 2):
                deltaNext = delta(end, points[i + 2])
                angleNext = atan2(deltaNext[1], deltaNext[0])
            if i == 0:
                anglePrev = angleCurrent

            startGuide = (angleCurrent - anglePrev) / 2
            endGuide = (angleCurrent - angleNext) / 2
            
            scale = hypot(deltaCurrent[0],deltaCurrent[1]) / 2
            
            midpoint = (start[0] + deltaCurrent[0] / 2, start[1] + deltaCurrent[1] / 2)

            geospace = GeoSpace(angleCurrent,scale, scale, midpoint, startGuide, endGuide)

            self.riblets.append(Riblet(geospace))

            anglePrev = angleCurrent
    
    def getLines(self):
        result = []
        for riblet in self.riblets:
            result.extend(riblet.getExtended(self.pattern, 0.3))
        return result
