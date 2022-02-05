
from math import floor
from geometry.point import Point
from hierarchy.pattern import Pattern
from hierarchy.curve import Curve
from hierarchy.ribbon import Ribbon


class Layer:

    def __init__(
            self,
            radius: float,
            width: float,
            pattern: Pattern,
            repeats: int = None) -> None:

        if repeats is None:
            repeats = int(4 + 16 * radius)

        n = max(64, int(radius * 16 + 48))
        curve = Curve(Point(radius, 0), closed=True)
        curve.extend(curve.arc(Point(-radius, 0),
                               amplitude=1,
                               subDivs=floor(n / 2)))
        curve.extend(curve.arc(Point(radius, 0),
                               amplitude=1,
                               subDivs=floor(n / 2)))
        self.ribbon = Ribbon(
            curve,
            pattern,
            closed=True,
            n=repeats,
            width=width)

    def render(self, display):
        return self.ribbon.render(display)
