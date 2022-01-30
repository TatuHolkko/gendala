
from math import sin, cos, pi
from feature import Feature
from typing import List
from curve import Curve
from ribbon import Ribbon
from geometry import Line, Pattern, Point


def ngon(n, radius) -> List[Point]:
    return [Point(radius * cos(x / n * 2 * pi),
                  radius * sin(x / n * 2 * pi)) for x in range(n)]


class Layer:

    def __init__(
            self,
            radius: float,
            width: float,
            pattern: Pattern,
            repeats:int = None) -> None:

        n = max(64, int(radius * 16 + 48))
        if repeats is None:
            repeats = int(4 + 16 * radius)

        points = ngon(n, radius)
        curve = Curve(points[0], closed=True)
        curve.extend(points[1:])
        self.ribbon = Ribbon(curve, pattern, closed=True, n=repeats)
        self.width = width
    
    def render(self, display):
        return self.ribbon.render(display, self.width)
