from copy import deepcopy
from math import ceil, floor
import random
from common.utility import multiplePair
from geometry.point import Point
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

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the generator

        Args:
            settings (Settings): Settings object
        """
        self.lastRepeats = 2
        self.featureGenerator = FeatureGenerator(settings=settings)
        self.repeatCoeff = settings.getItem(
            "Generator", "featureWidthCoeff", float)

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
        optimalRepeats = int(6.28 * (radius) / width / 2) * 2
        optimalRepeats = optimalRepeats / self.repeatCoeff

        deviation = (self.lastRepeats - optimalRepeats) / optimalRepeats
        if deviation < 0:
            repeats = 2 * self.lastRepeats
        elif deviation > 0.2:
            repeats = int(self.lastRepeats / 4 + optimalRepeats / 4) * 2
        repeats = max(8, repeats)
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

        complexity = random.randint(2, 8)
        superMirrored = coinFlip()
        divider = coinFlip()
        interContinuous = coinFlip()

        repeats = self.getRepeats(radius=radius, width=width)
        if repeats < complexity * 2:
            repeats = complexity * 2
        repeats = ceil(repeats / complexity) * complexity
        if not multiplePair(repeats, self.lastRepeats):
            divider = True
            width *= 0.9
        self.lastRepeats = repeats
        repeats = ceil(max(4, int(repeats / complexity)) / 2) * 2

        yEdge = None
        if interContinuous:
            yEdge = randomCoordinate()
        yInside = [
            randomCoordinate() if coinFlip() else None for _ in range(
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

        if divider:
            resultPattern.combine(horizontalLine(-1))
            if coinFlip():
                resultPattern.combine(horizontalLine(-0.95))


        l = Layer(
            radius=radius,
            width=width,
            pattern=resultPattern,
            repeats=repeats)
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
