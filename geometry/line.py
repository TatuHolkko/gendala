from geometry.point import Point


class Line:
    def __init__(self, p0: Point, p1: Point) -> None:
        self.p0 = p0
        self.p1 = p1

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Line):
            return False
        return self.p0 == __o.p0 and self.p1 == __o.p1

    def __hash__(self) -> int:
        return self.p0.__hash__() ^ self.p1.__hash__()

    def __repr__(self) -> str:
        return f"({self.p0.__repr__()},{self.p1.__repr__()})"
