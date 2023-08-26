import random
from common.settings import Settings
from common.utility import Logger
from generation.ribbon import RibbonGenerator
from geometry.point import Point
from hierarchy.feature import Feature
from generation.utility import check, sampleFromDistribution


class FeatureGenerator:
    """
    Generator for Feature objects
    """

    def __init__(self, settings: Settings, logger: Logger) -> None:
        """
        Initialize the generator

        Args:
            settings (Settings): Settings object
        """
        self.logger = logger
        self.ribbonGenerator = RibbonGenerator(settings, logger)
        self.pMirrorX = settings.getItem(
            "SimpleFeatures", "P_mirrorX", float)
        self.pMirrorY = settings.getItem(
            "SimpleFeatures", "P_mirrorY", float)
        self.connectionOverride = settings.getItem(
            "SimpleFeatures", "connectionOverridesMirror", bool)
        self.pdNRibbons = settings.getList(
            "SimpleFeatures", "PD_complexity", float)

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

        n = sampleFromDistribution(self.pdNRibbons)
        connectedLeft = random.choice(range(n))
        connectedRight = random.choice(range(n))
        for i in range(n):
            start = None
            end = None
            if i == connectedLeft and leftConnection:
                start = Point(-1, leftConnection)
            if i == connectedRight and rightConnection:
                end = Point(1, rightConnection)
            self.logger.layerPrint(f"\t\tGenerating Ribbon {i+1}/{n}...")
            feature.add(self.ribbonGenerator.getRibbon(start=start, end=end))
            self.logger.layerPrint(f"\t\tDone.")

        return feature
