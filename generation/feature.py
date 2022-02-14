import random
from common.settings import Settings
from generation.ribbon import RibbonGenerator
from geometry.point import Point
from hierarchy.feature import Feature
from generation.utility import coinFlip


class FeatureGenerator:
    """
    Generator for Feature objects
    """

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the generator

        Args:
            settings (Settings): Settings object
        """
        self.ribbonGenerator = RibbonGenerator(settings=settings)

    def getFeature(self,
                   leftConnection: float = None,
                   rightConnection: float = None) -> Feature:
        """
        Generate a random Feature

        Args:
            leftConnection (float): If given, y coordinate of left connection
            rightConnection (float): If given, y coordinate of right connection

        Returns:
            Feature: A random Feature
        """
        mirrorX = coinFlip()

        if leftConnection and (not rightConnection) and mirrorX:
            rightConnection = leftConnection
        elif rightConnection and (not leftConnection) and mirrorX:
            leftConnection = rightConnection
        elif rightConnection and leftConnection and (not leftConnection == rightConnection):
            mirrorX = False

        mirrorY = coinFlip()

        if mirrorY:
            if leftConnection:
                leftConnection = abs(leftConnection) - 0.5
            if rightConnection:
                rightConnection = abs(rightConnection) - 0.5

        feature = Feature(mirrorY=mirrorY, mirrorX=mirrorX)

        n = random.choice([1, 1, 1, 2])
        connectedLeft = random.choice(range(n))
        connectedRight = random.choice(range(n))
        for i in range(n):
            start = None
            end = None
            if i == connectedLeft and leftConnection:
                start = Point(-1, leftConnection)
            if i == connectedRight and rightConnection:
                end = Point(1, rightConnection)
            feature.add(self.ribbonGenerator.getRibbon(start=start, end=end))

        return feature
