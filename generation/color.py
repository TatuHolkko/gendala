import colorsys
import random
from typing import Tuple
from common.settings import Settings
from common.utility import Color, clamp, Logger
from generation.utility import coinFlip


class ColorGenerator:
    """
    Generator for background and foreground color pairs.
    """

    def __init__(self, settings: Settings, logger:Logger) -> None:
        """
        Initialize the Color generator object.

        Args:
            settings (Settings):  Settings object
        """
        self.logger = logger
        self.centerValueRange = settings.getList(
            "Colors", "centerValueRange", float)
        self.bgHueRange = settings.getList("Colors", "bgHueRange", float)
        self.bgHueDeviation = settings.getItem(
            "Colors", "bgHueDeviation", float)
        self.fgHueOffset = settings.getItem("Colors", "fgHueOffset", float)
        self.fgHueDeviation = settings.getItem(
            "Colors", "fgHueDeviation", float)

        self.hueDiffCoeff = settings.getItem("Colors", "hueDiffCoeff", float)
        self.satDiffCoeff = settings.getItem("Colors", "satDiffCoeff", float)
        self.valDiffCoeff = settings.getItem("Colors", "valDiffCoeff", float)
        self.visualDiffThreshold = settings.getItem(
            "Colors", "visualDiffThreshold", float)
        self.purityThreshold = settings.getItem(
            "Colors", "purityThreshold", float)

        while True:
            self.bg1 = self.randomColor(
                self.bgHueRange,
                (0.6, 0.8),
                (self.centerValueRange[0], self.centerValueRange[1]),
                allowPure=True)

            bg1Hue, _, _ = self.bg1.hsv()

            bg2HueMin = (bg1Hue * 360 - self.bgHueDeviation)
            bg2HueMax = (bg1Hue * 360 + self.bgHueDeviation)

            self.bg2 = self.randomColor(
                (bg2HueMin, bg2HueMax),
                (0.3, 0.7),
                (0, 0.2),
                allowPure=True)

            self.fg1 = self.fgFromBg(self.bg1)
            self.fg2 = self.fgFromBg(self.bg2)

            if self.visualDistance(self.bg1,
                                   self.fg1) < self.visualDiffThreshold:
                self.logger.layerPrint("\tForeground too similar to background, discarded.")
                continue
            if self.visualDistance(self.bg2,
                                   self.fg2) < self.visualDiffThreshold:
                self.logger.layerPrint("\tForeground too similar to background, discarded.")
                continue
            break

    def visualDistance(self, c1: Color, c2: Color) -> float:
        """
        Return a float representing the visual difference between
        the given colors.

        Args:
            c1 (Color): Color 1
            c2 (Color): Color 2

        Returns:
            float: Number representing the difference
        """
        h1, s1, v1 = c1.hsv()
        h2, s2, v2 = c2.hsv()
        hd = min(abs(h1 - h2), 1 - abs(h1 - h2))
        sd = abs(s1 - s2)
        vd = abs(v1 - v2)
        return hd * self.hueDiffCoeff + sd * self.satDiffCoeff + vd * self.valDiffCoeff

    def fgFromBg(self, bg: Color) -> Color:
        """
        Generate foreground color for a given background color.

        The hue of the returned color is selected away from the hue
        of the background.

        Args:
            bg (Color): Background color

        Returns:
            Color: Color that has different hue than background
        """
        bgHue, _, _ = bg.hsv()
        sign = 1 if coinFlip() else -1
        offset = (bgHue * 360 + sign * self.fgHueOffset)
        fgHueMax = (offset + self.fgHueDeviation)
        fgHueMin = (offset - self.fgHueDeviation)
        val = 1
        return self.randomColor(
            (fgHueMin, fgHueMax),
            (0.5, 0.7),
            (val, val))

    def randomColor(self,
                    hueRange: Tuple[float,
                                    float],
                    satRange: Tuple[float,
                                    float],
                    valRange: Tuple[float,
                                    float],
                    allowPure: bool = False) -> Color:
        """
        Generate a random color using ranges for the hsv values.

        The hue is shifted if it happens to be too pure red green or blue.

        Args:
            hueRange (Tuple[float,float]): Hue range (degrees)
            satRange (Tuple[float,float]): Saturation range (0 - 1)
            valRange (Tuple[float,float]): Value range (0 - 1)
            allowPure (bool): If false, pure colors are shifted a bit.

        Returns:
            Color: Generated color
        """
        hue = random.uniform(hueRange[0], hueRange[1]) % 360
        if not allowPure:
            hue = self.fixHue(hue=hue) / 360.0
        sat = clamp(random.uniform(satRange[0], satRange[1]), 0, 1)
        val = clamp(random.uniform(valRange[0], valRange[1]), 0, 1)
        rgb = colorsys.hsv_to_rgb(hue, sat, val)
        return Color(rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)

    def fixHue(self, hue: float) -> float:
        """
        If the given hue is too pure red, green or blue,
        it is shifted into a random direction.

        Args:
            hue (float): Hue (degrees)

        Returns:
            float: Hue that is guaranteed to not be pure red green or blue
        """
        sign = self.impurityDirection(hue=hue)
        if self.isPureHue(hue):
            hue = (hue + sign * self.purityThreshold) % 360
        return hue

    def impurityDirection(self, hue: float) -> int:
        """
        Calculate the shorter direction away from pure red green and blue.

        Args:
            hue (float): Hue (degrees)

        Returns:
            int: -1 or 1, representing the direction
        """
        hueMod = hue % 120
        if hueMod < self.purityThreshold:
            return 1
        else:
            return -1

    def isPureHue(self, hue: float) -> bool:
        """
        Return true if the hue is too pure.

        Args:
            hue (float): Hue (degrees)

        Returns:
            bool: True if the hue is too pure
        """
        dRed = min(hue, 360 - hue)
        dGreen = min(abs(hue - 120), 360 - abs(hue - 120))
        dBlue = min(abs(hue - 240), 360 - abs(hue - 240))
        return (dRed < self.purityThreshold or
                dGreen < self.purityThreshold or
                dBlue < self.purityThreshold)

    def getBackgroundColors(self) -> Tuple[Color, Color]:
        """
        Get the generated background colors.

        Returns:
            Tuple[Color, Color]: Background colors
        """
        return (self.bg1, self.bg2)

    def getLineColors(self) -> Tuple[Color, Color]:
        """
        Get the generated foreground colors.

        Returns:
            Tuple[Color, Color]: Foreground colors
        """
        return (self.fg1, self.fg2)
