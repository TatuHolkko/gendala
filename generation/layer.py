from copy import deepcopy
from math import ceil, floor
from common.utility import multiplePair
from geometry.point import Point
from generation.feature import FeatureGenerator
from generation.utility import check, sampleFromDistribution, randomCoordinate
from generation.pattern import randomComplexPattern
from common.settings import Settings
from hierarchy.curve import Curve
from hierarchy.layer import Layer
from hierarchy.pattern import Pattern
from hierarchy.ribbon import Ribbon


class LayerGenerator:
    """
    Generator for Layer objects
    """

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the generator

        Args:
            settings (Settings): Settings object
        """
        self.lastRepeats = 2
        self.featureGenerator = FeatureGenerator(settings=settings)
        self.repeatCoeff = settings.getItem(
            "Layers", "featureWidthCoeff", float)
        self.pDivider = settings.getItem(
            "Layers", "P_divider", float)
        self.forceDivider = settings.getItem(
            "Layers", "fractionBoundaryForceDivider", bool)
        self.dividerWidth = settings.getItem(
            "Layers", "dividerWidth", float)
        self.dividerPadding = settings.getItem(
            "Layers", "dividerPadding", float)
        self.pdComplexity = settings.getList(
            "ComplexFeatures", "PD_complexity", float)
        self.pInterCont = settings.getItem(
            "ComplexFeatures", "P_interContinuous", float)
        self.pIntraCont = settings.getItem(
            "ComplexFeatures", "P_intraContinuous", float)

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
        optimalRepeats = int(6.28 * (radius) / width / 4) * 2
        optimalRepeats = optimalRepeats / self.repeatCoeff

        deviation = (self.lastRepeats - optimalRepeats) / optimalRepeats
        if deviation < 0:
            repeats = 2 * self.lastRepeats
        elif deviation > 0.2:
            repeats = int(self.lastRepeats / 4 + optimalRepeats / 4) * 2
        repeats = max(4, repeats)
        return repeats

    def getLayer(
            self,
            radius: float,
            width: float) -> Layer:
        """
        Generate a random Layer

        If repeats are not given, an optimal amount is calculated.

        Args:
            radius (float): Radius of the layer
            width (float): Width of the layer

        Returns:
            Layer: A random Layer
        """

        complexity = 2 * sampleFromDistribution(self.pdComplexity)

        divider = check(self.pDivider)

        repeats = self.getRepeats(radius=radius, width=width)
        if repeats < complexity * 2:
            repeats = complexity * 2
        repeats = ceil(repeats / complexity) * complexity
        if self.forceDivider and not multiplePair(repeats, self.lastRepeats):
            divider = True
        self.lastRepeats = repeats
        repeats = ceil(max(4, int(repeats / complexity)) / 2) * 2

        yEdge = None
        if check(self.pInterCont):
            yEdge = randomCoordinate()
        yInside = [
            randomCoordinate() if check(
                self.pIntraCont) else None for _ in range(
                complexity - 1)]
        connections = [yEdge]
        connections.extend(yInside)
        connections.append(yEdge)

        resultPattern = Pattern()

        centerIndex = floor((complexity - 1) / 2)
        center = self.featureGenerator.getFeature(
            connections[centerIndex],
            connections[centerIndex],
            forceXMirror=True
        ).getPattern()

        patternWidth = 0
        if complexity % 2 != 0:
            patternWidth = 2
        else:
            patternWidth = 4
            mirror(center)

        resultPattern.combine(center)

        i = centerIndex
        while i > 0:
            feature = self.featureGenerator.getFeature(
                leftConnection=connections[i],
                rightConnection=connections[i - 1]
            )

            surround(resultPattern, patternWidth, feature.getPattern())
            patternWidth += 4
            i -= 1

        resultPattern.offsetX(-complexity)
        resultPattern.scaleX(1 / complexity)
        resultPattern.scaleYToLimits()

        if divider:
            dividerSpace = self.dividerWidth + self.dividerPadding * 2
            dividerY = 1 - dividerSpace / 2
            dividerCurve = Curve(Point(-1, -dividerY))
            dividerCurve.extend(dividerCurve.line(Point(1, -dividerY)))
            dividerPattern = randomComplexPattern()
            dividerRibbon = Ribbon(
                dividerCurve,
                dividerPattern,
                closed=False,
                width=self.dividerWidth / 2,
                n=complexity * 3)
            resultPattern.scaleY(1 - dividerSpace / 2)
            resultPattern.offsetY(dividerSpace / 2)
            resultPattern.combine(dividerRibbon.getPattern())

        l=Layer(
            radius = radius,
            width = width,
            pattern = resultPattern,
            repeats = repeats)
        return l


def mirror(pattern: Pattern) -> None:
    """
    Combine an unscaled mirror pattern into the given pattern.

    Args:
        pattern (Pattern): Pattern to mirror
    """

    mirroredPattern=deepcopy(pattern)
    mirroredPattern.scaleX(-1)
    mirroredPattern.offsetX(1)

    pattern.offsetX(-1)

    pattern.combine(mirroredPattern)


def surround(center: Pattern, centerWidth: float, edges: Pattern) -> None:
    """
    Combine the edge Pattern (one side mirrored) on both sides of center Pattern

    Args:
        center (Pattern): Center Pattern
        centerWidth (float): Width of center Pattern
        edges (Pattern): Edge Pattern
    """

    rightMirror=deepcopy(edges)
    rightMirror.scaleX(-1)

    leftMirror=deepcopy(edges)

    offset=centerWidth / 2 + 1

    leftMirror.offsetX(-offset)
    rightMirror.offsetX(offset)

    center.combine(leftMirror)
    center.combine(rightMirror)
