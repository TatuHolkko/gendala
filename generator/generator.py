import random
from ribbon import Ribbon
from feature import Feature
from generator.patternGenerators import randomPattern
from generator.curveGenerators import randomCurve
from utility import coinFlip


class Generator:

    def __init__(self) -> None:
        pass

    def getFeature(self):
        feature = Feature(mirrorY=coinFlip(), mirrorX=coinFlip())
        n = random.randint(1,1)
        for _ in range(n):
            feature.add(self.getRibbon())
        return feature


    def getRibbon(self):
        closed = False #coinFlip()
        curve = randomCurve(closed=closed)
        curve.round()
        pattern = randomPattern()
        n = random.randint(1, 10)
        taperLength = max(0, random.random() - 0.5)
        return Ribbon(
            curve=curve,
            pattern=pattern,
            closed=closed,
            taperLength=taperLength,
            n=n)
