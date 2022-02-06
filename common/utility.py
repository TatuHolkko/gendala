from typing import List, TypeVar
import random

T = TypeVar('T')

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
    Return sign of given value as an integers

    Args:
        value (float): value

    Returns:
        int: -1 or 1
    """
    return int(value >= 0) * 2 - 1

def tuplify(lst: List) -> tuple:
    """
    Convert list and its elements recursively to tuple

    Args:
        lst (List): List to convert

    Returns:
        tuple: Tuple containing all items of given List
    """
    return tuple(tuplify(i) if isinstance(i, list) else i for i in lst)

def listify(tpl: tuple) -> List:
    """
    Convert tuple and its elements recursively to List

    Args:
        lst (tuple): tuple to convert

    Returns:
        List: List containing all items of given tuple
    """
    return list(listify(i) if isinstance(i, tuple) else i for i in tpl)

def gradient(v1:T, v2:T, s: float) -> T:
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

def coinFlip() -> bool:
    """
    Return True or False, both as likely.

    Returns:
        bool: Result
    """
    return random.choice([True, False])