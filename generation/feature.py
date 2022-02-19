import random
from common.settings import Settings
from generation.ribbon import RibbonGenerator
from geometry.point import Point
from hierarchy.feature import Feature
from generation.utility import check, checkDistribution


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
        self.pMirrorX = settings.getItem(
            "SimpleFeatures", "P_mirrorX", float)
        self.pMirrorY = settings.getItem(
            "SimpleFeatures", "P_mirrorY", float)
        self.connectionOverride = settings.getItem(
            "SimpleFeatures", "connectionOverridesMirror", bool)
        self.pdNRibbons = settings.getList(
            "SimpleFeatures", "PD_numberOfRibbons", float)


    def getFeature(self,
                   leftConnection: float = None,
                   rightConnection: float = None,
                   forceXMirror: bool = False) -> Feature:
        """
        Generate a random Feature

        Args:
            leftConnection (float): If given, y coordinate of left connection
            rightConnection (float): If given, y coordinate of right connection
            forceXMirror (bool): if true, X will always be mirrored

        Returns:
            Feature: A random Feature
        """
        mirrorX = check(self.pMirrorX) or forceXMirror
        mirrorY = check(self.pMirrorY)

        if leftConnection and (not rightConnection) and mirrorX:
            rightConnection = leftConnection
        elif rightConnection and (not leftConnection) and mirrorX:
            leftConnection = rightConnection
        elif rightConnection and leftConnection and (not leftConnection == rightConnection):
            # both connections given and they are not equal
            if self.connectionOverride:
                leftConnection = rightConnection
            else:
                mirrorX = False

        if mirrorY:
            if leftConnection:
                leftConnection = abs(leftConnection) - 0.5
            if rightConnection:
                rightConnection = abs(rightConnection) - 0.5

        feature = Feature(mirrorY=mirrorY, mirrorX=mirrorX)

        n = checkDistribution(self.pdNRibbons)
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
