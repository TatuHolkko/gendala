from math import ceil
from generation.feature import FeatureGenerator
from generation.utility import coinFlip, randomCoordinate
from generation.pattern import horizontalLine
from common.settings import Settings
from hierarchy.layer import Layer
from hierarchy.pattern import Pattern

class LayerGenerator:
    """
    Generator for Layer objects
    """

    def __init__(self, settings:Settings) -> None:
        """
        Initialize the generator

        Args:
            settings (Settings): Settings object
        """
        self.lastRepeats = 2
        self.featureGenerator = FeatureGenerator(settings=settings)
        self.repeatCoeff = settings.getItem("Generator", "featureWidthCoeff", float)

    def getRepeats(self, radius: float, width: float) -> int:
        """
        Get the number of repeated patterns for a given radius and width

        Args:
            radius (float): Radius of the center of the layer
            width (float): Width of the layer

        Returns:
            int: Number of repeats
        """
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
        """
        Generate a random Layer

        If repeats are not given, an optimal amount is calculated.

        Args:
            radius (float): Radius of the layer
            width (float): Width of the layer
            repeats (int, optional): Number of pattern repeats. Defaults to None.

        Returns:
            Layer: A random Layer
        """

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