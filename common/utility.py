from __future__ import annotations
import colorsys
from typing import List, TypeVar

T = TypeVar('T')

"""
Generally useful functions
"""

def multiplePair(val1:int, val2:int) -> bool:
    """
    Return true if val1 is a multiple of val2 or vice versa

    Args:
        val1 (int): Value 1
        val2 (int): Value 2

    Returns:
        bool: True if val1 is a multiple of val2 or vice versa
    """
    return ((float(val1)/val2) % 1 == 0) or ((float(val2)/val1) % 1 == 0)

def clamp(value: float, minLim: float, maxLim: float) -> float:
    """
    Return value clamped to minimum and maximum limits

    Args:
        value (float): Value to clamp
        minLim (float): Minimum value
        maxLim (float): Maximum value

    Returns:
        float: value between minLim and maxLim
    """
    return min(max(value, minLim), maxLim)


def sign(value: float) -> int:
    """
    Return sign of given value as an integer

    Args:
        value (float): value

    Returns:
        int: -1 or 1
    """
    return int(value >= 0) * 2 - 1


def tuplify(lst: List) -> tuple:
    """
    Convert list and its elements recursively to tuple.

    If the given list is a list of lists, all sub lists will be tuplified
    too.

    Args:
        lst (List): List to convert

    Returns:
        tuple: Tuple containing all items of given List
    """
    return tuple(tuplify(i) if isinstance(i, list) else i for i in lst)


def listify(tpl: tuple) -> List:
    """
    Convert tuple and its elements recursively to List.

    If the given tuple is a tuple of tuples, all sub tuples will be listified
    too.

    Args:
        lst (tuple): tuple to convert

    Returns:
        List: List containing all items of given tuple
    """
    return list(listify(i) if isinstance(i, tuple) else i for i in tpl)


def gradient(v1: T, v2: T, s: float) -> T:
    """
    Return a value between v1 and v2, defined by s.

    s=0 will return v1
    s=1 will return v2

    Values for s=(0,1) are linearly interpolated.

    T must implement __mul__(float), __add__(T), __sub__(T)

    Args:
        v1 (T): Value 1
        v2 (T): Value 2
        s (float): Value between 0 and 1

    Returns:
        T: Interpolated value
    """
    d = v2 - v1
    return v1 + d * s

class Logger:
    def __init__(self) -> None:
        self.maxLayer = 1
        self.layer = 1
    
    def setLayer(self, value):
        self.layer = value

    def setMaxLayer(self, value):
        self.maxLayer = value

    def layerPrint(self, txt):
        print("[" + str(self.layer).zfill(2) + "/" + str(self.maxLayer).zfill(2) + "] " + txt)

class Color:
    """
    Color defines three rgb channels
    """

    def __init__(self, r: int, g: int, b: int) -> None:
        """
        Intialize the color.

        Each value is clamped between 0 and 255.

        Args:
            r (int): Red value
            g (int): Green value
            b (int): Blue value
        """
        self.r = int(clamp(0, 255, r))
        self.g = int(clamp(0, 255, g))
        self.b = int(clamp(0, 255, b))
    
    def hsv(self) -> tuple[float, float, float]:
        """
        Get a tuple of the three hsv channels

        Returns:
            tuple[float, float, float]: (r,g,b)
        """
        return colorsys.rgb_to_hsv(self.r, self.g, self.b)

    def rgb(self) -> tuple[float, float, float]:
        """
        Get a tuple of the three rgb channels

        Returns:
            tuple[float, float, float]: (r,g,b)
        """
        return (self.r, self.g, self.b)

    def __add__(self, other: Color):
        return Color(
            r=self.r + other.r,
            g=self.g + other.g,
            b=self.b + other.b
        )

    def __sub__(self, other: Color):
        return Color(
            r=self.r - other.r,
            g=self.g - other.g,
            b=self.b - other.b
        )

    def __mul__(self, scale: float):
        return Color(
            r=self.r * scale,
            g=self.g * scale,
            b=self.b * scale
        )
