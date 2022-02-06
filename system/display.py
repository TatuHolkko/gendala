import os                                           # nopep8
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # nopep8
import pygame                                       # nopep8
import pygame.gfxdraw                               # nopep8

from copy import deepcopy
from typing import List
from geometry.geospace import GeoSpace, GeoSpaceStack
from geometry.line import Line
from geometry.point import Point
from common.utility import gradient

antiAlias = True


class Display:
    """
    Display provides functions for rendering lines.
    """

    def __init__(self, surf, autoFlush: bool = True) -> None:
        """
        Initialize the Display object.

        Args:
            surf (pygame Surface): Surface to render into.
            autoFlush (bool): Whether to update the screen after each line
        """
        self.surf = surf
        self.width = surf.get_width()
        self.height = surf.get_height()
        self.autoFlush = autoFlush
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
        self.color = [255, 255, 255]

    def drawLine(self, line: Line) -> None:
        """
        Draw a line

        Args:
            line (Line):  Line to draw
        """
        if self.renderDisabled:
            return

        self.lineBuffer.append(deepcopy(line))
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
            pos0 = self.geoSpaceStack.getGlobalPos(line.p0)
            pos1 = self.geoSpaceStack.getGlobalPos(line.p1)
            if antiAlias:
                self.drawAALine(pos0, pos1)
            else:
                pygame.draw.line(
                    self.surf,
                    (self.color[0],
                     self.color[1],
                     self.color[2]),
                    (round(pos0.x),
                     round(pos0.y)),
                    (round(pos0.x),
                     round(pos0.y)))
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
            (self.color[0],
             self.color[1],
             self.color[2]))

    def clear(self) -> None:
        """
        Clear the screen
        """
        self.lineBuffer = []
        self.surf.fill((0, 0, 0))
        pygame.display.update()

    def setColor(self, r: int, g: int, b: int) -> None:
        """
        Set line color

        Args:
            r (int): Red
            g (int): Green
            b (int): Blue
        """
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b

    def drawDebugGrid(self) -> None:
        """
        Draw a red unit square with x and y axes
        """
        tempcolor = deepcopy(self.color)
        self.setColor(255, 0, 0)
        # unit square
        self.drawLine(Line(Point(1, 1), Point(-1, 1)))
        self.drawLine(Line(Point(-1, 1), Point(-1, -1)))
        self.drawLine(Line(Point(-1, -1), Point(1, -1)))
        self.drawLine(Line(Point(1, -1), Point(1, 1)))
        # x and y axis
        self.drawLine(Line(Point(0, 1), Point(0, -1)))
        self.drawLine(Line(Point(1, 0), Point(-1, 0)))
        self.setColor(tempcolor[0], tempcolor[1], tempcolor[2])

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
