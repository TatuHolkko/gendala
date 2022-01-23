from feature import Feature
from geospace import GeoSpace
from ribbon import Ribbon
from curve import Curve
import pygame
import math
import os

from utility import Point, patternFromPoints
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


def ngon(n):
    return [[math.cos(x / n * 2 * math.pi),
             math.sin(x / n * 2 * math.pi)] for x in range(n)]


def main():
    pygame.init()
    pygame.display.set_caption("Fractal curve generator")

    surf = pygame.display.set_mode(size=(400, 400))

    debug_square = [[[-1, 1], [1, 1]], [[1, 1], [1, -1]],
                    [[1, -1], [-1, -1]], [[-1, -1], [-1, 1]]]

    grid = [
        #[[-1, 0], [0, 1]],
        [[-1, -1], [1, 1]], # diag 1
        #[[1, -1], [-1, 1]], # diag 2
        #[[0, -1], [1, 0]],
        #[[0,-1], [1,1]],
        [[-1, 1], [1, 1]],  # top hor
        #[[-1, 0], [1, 0]],  # mid hor
        [[-1, -1], [1, -1]],  # bot hor
        #[[0, 1], [0, -1]], #center ver
        #[[-1, 1], [-1, -1]], #left ver
        #[[1, 1], [1, -1]], #right ver
    ]

    curv = Curve(Point(-1,0))

    curv.extend(curv.sine(Point(1,0), subDivs=7, amplitude=0.5))
    curv.extend(curv.arc(Point(0,-1), curvature=1))

    curv.round()

    feat = Feature(mirrorX=True, mirrorY=True)

    rib = Ribbon(curv, patternFromPoints(grid), closed=False, n=12)

    feat.add(rib)

    toDraw = feat.render(0.1)

    for stroke in debug_square:
        pygame.draw.line(
            surf,
            (255,
             0,
             0),
            (round(200 + stroke[0][0] * 50),
             round(200 + -stroke[0][1] * 50)),
            (round(200 + stroke[1][0] * 50),
             round(200 + -stroke[1][1] * 50)))

    for stroke in toDraw:
        pygame.draw.line(
            surf,
            (255,
             255,
             255),
            (round(200 + stroke.p0.x * 50),
             round(200 + -stroke.p0.y * 50)),
            (round(200 + stroke.p1.x * 50),
             round(200 + -stroke.p1.y * 50)))

    pygame.display.update()
    exited = False
    while not exited:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exited = True


main()
