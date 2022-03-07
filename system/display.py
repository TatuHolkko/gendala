import os

from generation.color import ColorGenerator                                           # nopep8
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # nopep8
import pygame                                       # nopep8
import pygame.gfxdraw                               # nopep8

from math import hypot
from typing import List
from geometry.geospace import GeoSpace, GeoSpaceStack
from geometry.line import Line
from geometry.point import Point
from common.utility import Color, gradient
from common.settings import Settings


class Display:
    """
    Display provides functions for rendering lines.
    """

    def __init__(self, surf, settings: Settings) -> None:
        """
        Initialize the Display object.

        Args:
            surf (pygame Surface): Surface to render into.
            settings (Settings):  Settings object
        """
        self.surf = surf
        self.width = surf.get_width()
        self.height = surf.get_height()
        self.settings = settings
        self.antialiasing = settings.getBool("Graphics", "antialiasing")
        self.autoFlush = settings.getBool("Graphics", "autoFlush")
        self.autoColor = True
        self.scale = min(self.width, self.height) / 3
        self.lineBuffer: List[Line] = []
        self.renderDisabled = False
        self.geoSpace = GeoSpace(
            origin=Point(self.width / 2,
                         self.height / 2),
            yScale=-self.scale,
            xScale=self.scale)
        self.geoSpaceStack = GeoSpaceStack()
        self.geoSpaceStack.push(self.geoSpace)
        self.bgC0 = None
        self.bgC1 = None
        self.fgC0 = None
        self.fgC1 = None
        self.generateColors()
        self.lineColor = Color(255, 255, 255)

    def drawLine(self, line: Line) -> None:
        """
        Draw a line.

        Args:
            line (Line):  Line to draw
        """
        if self.renderDisabled:
            return

        pos0 = self.geoSpaceStack.getGlobalPos(line.p0)
        pos1 = self.geoSpaceStack.getGlobalPos(line.p1)

        self.lineBuffer.append(Line(pos0, pos1))

        if self.autoFlush:
            self.flushBuffer()

    def maxRadius(self) -> float:
        """
        Return the distance from center of screen
        to the corner in the geospace of the screen.

        Returns:
            float: Distance from center to corner in the geospace of the screen
        """
        diagonal = hypot(self.width, self.height)
        return diagonal / self.scale / 2

    def setAutoFlush(self, value: bool) -> None:
        """
        Set the auto flushing feature to True or False.

        Args:
            value (bool): Value
        """
        self.autoFlush = value

    def disableRender(self) -> None:
        """
        Disable rendering.
        """
        self.renderDisabled = True

    def enableRender(self) -> None:
        """
        Enable rendering.
        """
        self.renderDisabled = False

    def flushBuffer(self) -> None:
        """
        Draw buffered lines and clear the buffer.
        """
        for line in self.lineBuffer:
            pos0 = line.p0
            pos1 = line.p1
            if self.antialiasing:
                self.drawAALine(pos0, pos1)
            else:
                pygame.draw.line(
                    self.surf,
                    self.getFgColor(gradient(pos0, pos1, 0.5)).rgb(),
                    (round(pos0.x),
                     round(pos0.y)),
                    (round(pos1.x),
                     round(pos1.y)))
        self.lineBuffer = []
        pygame.display.update()

    def drawAALine(self, p1: Point, p2: Point) -> None:
        """
        Draw antialiased line from p1 to p2.

        Args:
            p1 (Point): Point 1
            p2 (Point): Point 2
        """
        mid = gradient(p1, p2, 0.5)
        c = self.getFgColor(mid)
        pygame.gfxdraw.aatrigon(
            self.surf,
            round(p1.x),
            round(p1.y),
            round(mid.x),
            round(mid.y),
            round(p2.x),
            round(p2.y),
            c.rgb())

    def getFgColor(self, p: Point) -> Color:
        """
        Get the foreground color at point p.

        Args:
            p (Point): Foreground point

        Returns:
            Color: Foreground color
        """
        if self.autoColor:
            center = Point(self.width / 2, self.height / 2)
            d = center.distanceTo(p)
            maxD = hypot(self.width, self.height) / 2
            return gradient(self.fgC0, self.fgC1, d / maxD)
        else:
            return self.lineColor

    def clear(self) -> None:
        """
        Fill the screen with black color.
        """
        self.lineBuffer = []
        c1 = Color(0, 0, 0)
        self.surf.fill(c1.rgb())
        pygame.display.update()

    def gradient(self) -> None:
        """
        Draw a radial gradient background.
        """
        self.lineBuffer = []
        diag = hypot(self.width, self.height)
        maxR = int(diag / 2)
        c0 = self.bgC0
        c1 = self.bgC1
        self.surf.fill(c1.rgb())
        for i in reversed(range(maxR)):
            c = gradient(c0, c1, i / maxR)
            x = int(self.width / 2)
            y = int(self.height / 2)
            pygame.gfxdraw.aacircle(self.surf, x, y, i, c.rgb())
            pygame.gfxdraw.filled_circle(self.surf, x, y, i, c.rgb())
        pygame.display.update()

    def generateColors(self) -> None:
        """
        Generate and update background and foreground color pairs.
        """
        print("Generating colors...")
        colorGen = ColorGenerator(settings=self.settings)
        print("Done.")
        self.bgC0, self.bgC1 = colorGen.getBackgroundColors()
        self.fgC0, self.fgC1 = colorGen.getLineColors()

    def setColor(self, r: int, g: int, b: int) -> None:
        """
        Set foreground color.

        Args:
            r (int): Red
            g (int): Green
            b (int): Blue
        """
        self.autoColor = False
        self.lineColor.r = r
        self.lineColor.g = g
        self.lineColor.b = b

    def setAutoColor(self) -> None:
        """
        Set autocoloring to true of false.

        If autocoloring is on, colors are randomly generated.
        """
        self.autoColor = True

    def drawDebugGrid(self) -> None:
        """
        Draw a red unit square with x and y axes.
        """
        # unit square
        self.drawLine(Line(Point(1, 1), Point(-1, 1)))
        self.drawLine(Line(Point(-1, 1), Point(-1, -1)))
        self.drawLine(Line(Point(-1, -1), Point(1, -1)))
        self.drawLine(Line(Point(1, -1), Point(1, 1)))
        # x and y axis
        self.drawLine(Line(Point(0, 1), Point(0, -1)))
        self.drawLine(Line(Point(1, 0), Point(-1, 0)))

    def pushGeoSpace(self, geoSpace: GeoSpace) -> None:
        """
        Push a geospace to the stack.

        Args:
            geoSpace (GeoSpace): GeoSpace to push
        """
        self.geoSpaceStack.push(geoSpace)

    def popGeoSpace(self) -> None:
        """
        Pop the last GeoSpace
        """
        self.geoSpaceStack.pop()
