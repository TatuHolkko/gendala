from math import ceil
from generation.feature import FeatureGenerator
from generation.utility import coinFlip, randomCoordinate
from generation.pattern import horizontalLine
from common.settings import Settings
from hierarchy.layer import Layer
from hierarchy.pattern import Pattern

class LayerGenerator:

    def __init__(self, settings:Settings) -> None:
        self.lastRepeats = 2
        self.featureGenerator = FeatureGenerator(settings=settings)
        self.repeatCoeff = settings.getItem("Generator", "featureWidthCoeff", float)

    def getRepeats(self, radius: float, width: float) -> int:
        repeats = self.lastRepeats
        optimalRepeats = int(6.28 * (radius + 0.1) / width / 2) * 2
        optimalRepeats = optimalRepeats / self.repeatCoeff

        deviation = (self.lastRepeats - optimalRepeats) / optimalRepeats
        if deviation < -0.6:
            repeats = 2 * self.lastRepeats
        elif deviation > 0.2:
            repeats = int(self.lastRepeats / 4 + optimalRepeats / 4) * 2
        if coinFlip():
            repeats = int(repeats / 4) * 2
        repeats = max(8, repeats)
        return repeats

    def getLayer(
                self,
                radius: float,
                width: float,
                repeats: int = None) -> Layer:

            divider = coinFlip()

            if not repeats:
                repeats = self.getRepeats(radius=radius, width=width)
            
            if ((repeats / self.lastRepeats) % 1 != 0) and ((self.lastRepeats / repeats) % 1 != 0):
                divider = True

            self.lastRepeats = repeats
                
            yEdge = None
            yCenter = None
            if coinFlip():
                yEdge = randomCoordinate()
            if coinFlip():
                yCenter = randomCoordinate()

            f1 = self.featureGenerator.getFeature(leftConnection=yEdge, rightConnection=yCenter)
            f2 = self.featureGenerator.getFeature(leftConnection=yCenter, rightConnection=yEdge)

            pat1 = f1.getPattern()

            pat2 = f2.getPattern()

            pat2.offsetX(2)

            pat1.combine(pat2)
            pat1.offsetX(-1)
            pat1.scaleX(0.5)

            if True:
                pat1.offsetX(-1)
                mirror = Pattern()
                mirror.combine(pat1)
                mirror.scaleX(-1)
                pat1.combine(mirror)
                pat1.scaleX(0.5)

            if divider:
                pat1.combine(horizontalLine(-1))

            l = Layer(
                radius=radius,
                width=width,
                pattern=pat1,
                repeats=ceil(
                    repeats / 2))
            return l