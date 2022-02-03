import os                                           # nopep8
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # nopep8
import pygame                                       # nopep8
from copy import deepcopy
from typing import List
from geospace import GeoSpace, GeoSpaceStack
from geometry import Line, Point


class Display:

    def __init__(self, surf) -> None:
        self.surf = surf
        self.width = surf.get_width()
        self.height = surf.get_height()
        self.scale = min(self.width, self.height) / 3
        self.lineBuffer: List[Line] = []
        self.autoFlush = False
        self.geoSpace = GeoSpace()
        self.geoSpaceStack = GeoSpaceStack()
        self.geoSpaceStack.push(self.geoSpace)
        self.color = [255, 255, 255]

    def drawLine(self, line):
        self.lineBuffer.append(deepcopy(line))
        if self.autoFlush:
            self.flushBuffer()

    def setAutoFlush(self, value):
        self.autoFlush = value

    def flushBuffer(self):
        for line in self.lineBuffer:
            pos0 = self.geoSpaceStack.getGlobalPos(line.p0)
            pos1 = self.geoSpaceStack.getGlobalPos(line.p1)
            pygame.draw.line(
                self.surf,
                (self.color[0],
                 self.color[1],
                 self.color[2]),
                (round(self.width / 2 + pos0.x * self.scale),
                 round(self.height / 2 - pos0.y * self.scale)),
                (round(self.width / 2 + pos1.x * self.scale),
                 round(self.height / 2 - pos1.y * self.scale)))
        self.lineBuffer = []
        pygame.display.update()
    
    def clear(self):
        self.lineBuffer = []
        self.surf.fill((0,0,0))
        pygame.display.update()

    def setColor(self, r, g, b):
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b

    def drawDebugGrid(self):
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

    def pushGeoSpace(self, geoSpace):
        self.geoSpaceStack.push(geoSpace)

    def popGeoSpace(self):
        self.geoSpaceStack.pop()
