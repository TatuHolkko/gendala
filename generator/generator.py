import random
from curve import GeometryException
from ribbon import Ribbon
from feature import Feature
from generator.patternGenerators import centerLine, randomPattern
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
        closed = coinFlip()
        curve = None
        while(True):
            curve = randomCurve(closed=closed)
            try:
                curve.round()
            except GeometryException:
                continue
            break
        pattern = randomPattern()
        n = random.randint(1, 10)
        taperLength = max(0, random.random() - 0.5)
        return Ribbon(
            curve=curve,
            pattern=pattern,
            closed=closed,
            taperLength=taperLength,
            n=n)
