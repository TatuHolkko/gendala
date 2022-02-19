import os                                           # nopep8
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # nopep8
import pygame                                       # nopep8
import pygame.gfxdraw                               # nopep8

from math import hypot
from typing import List
from geometry.geospace import GeoSpace, GeoSpaceStack
from geometry.line import Line
from geometry.point import Point
from common.utility import Color, gradient
from common.settings import Settings                                           # nopep8


class Display:
    """
    Display provides functions for rendering lines.
    """

    def __init__(self, surf, settings:Settings) -> None:
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
        self.lineColor = Color(255, 255, 255)

    def drawLine(self, line: Line) -> None:
        """
        Draw a line

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

    def setAutoFlush(self, value: bool) -> None:
        """
        Set the auto flushing feature to True or False

        Args:
            value (bool): Value
        """
        self.autoFlush = value

    def disableRender(self) -> None:
        """
        Disable rendering
        """
        self.renderDisabled = True

    def enableRender(self) -> None:
        """
        Enable rendering
        """
        self.renderDisabled = False

    def flushBuffer(self) -> None:
        """
        Draw buffered lines and clear the buffer
        """
        for line in self.lineBuffer:
            pos0 = line.p0
            pos1 = line.p1
            if self.antialiasing:
                self.drawAALine(pos0, pos1)
            else:
                pygame.draw.line(
                    self.surf,
                    self.lineColor.get(),
                    (round(pos0.x),
                     round(pos0.y)),
                    (round(pos1.x),
                     round(pos1.y)))
        self.lineBuffer = []
        pygame.display.update()

    def drawAALine(self, p1: Point, p2: Point) -> None:
        mid = gradient(p1, p2, 0.5)
        pygame.gfxdraw.aatrigon(
            self.surf,
            round(p1.x),
            round(p1.y),
            round(mid.x),
            round(mid.y),
            round(p2.x),
            round(p2.y),
            self.lineColor.get())

    def clear(self) -> None:
        """
        Clear the screen
        """
        self.lineBuffer = []
        c1 = Color(0, 0, 0)
        self.surf.fill(c1.get())
        pygame.display.update()

    def gradient(self) -> None:
        """
        Draw a radial gradient background
        """
        self.lineBuffer = []
        diag = hypot(self.width, self.height)
        maxR = int(diag / 2)
        c0 = Color(232, 61, 19)
        c1 = Color(0, 0, 0)
        self.surf.fill(c1.get())
        for i in reversed(range(maxR)):
            c = gradient(c0, c1, i / maxR)
            x = int(self.width/2)
            y = int(self.height/2)
            pygame.gfxdraw.aacircle(self.surf, x, y, i, c.get())
            pygame.gfxdraw.filled_circle(self.surf, x, y, i, c.get())
        pygame.display.update()

    def setColor(self, r: int, g: int, b: int) -> None:
        """
        Set line color

        Args:
            r (int): Red
            g (int): Green
            b (int): Blue
        """
        self.lineColor.r = r
        self.lineColor.g = g
        self.lineColor.b = b

    def drawDebugGrid(self) -> None:
        """
        Draw a red unit square with x and y axes
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
        Push a geospace to the stack

        Args:
            geoSpace (GeoSpace): GeoSpace to push
        """
        self.geoSpaceStack.push(geoSpace)

    def popGeoSpace(self) -> None:
        """
        Pop the last GeoSpace
        """
        self.geoSpaceStack.pop()
