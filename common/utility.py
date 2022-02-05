from typing import List
import random

def clamp(value: float, minLim: float, maxLim: float) -> float:
    return min(max(value, minLim), maxLim)

def sign(value: float) -> int:
    return int(value >= 0) * 2 - 1

def tuplify(lst: List) -> tuple:
    # convert list to tuple
    return tuple(tuplify(i) if isinstance(i, list) else i for i in lst)

def listify(tpl: tuple) -> List:
    # convert tuple to list
    return list(listify(i) if isinstance(i, tuple) else i for i in tpl)

def gradient(v1, v2, s: float) -> float:
    d = v2 - v1
    return v1 + d * s

def coinFlip() -> bool:
    return random.choice([True, False])
