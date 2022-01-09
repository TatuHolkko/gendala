from geospace import GeoSpace
from ribbon import Ribbon
from curve import arc
import pygame
import math
import os
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
        #[[-1, -1], [1, 1]],
        #[[0, -1], [1, 0]],
        #[[0,-1], [1,1]],
        [[-1, 1], [1, 1]],  # top hor
        #[[-1, 0], [1, 0]],  # mid hor
        [[-1, -1], [1, -1]],  # bot hor
        #[[0, 1], [0, -1]], #center ver
        [[-1, 1], [-1, -1]], #left ver
        [[1, 1], [1, -1]], #right ver
    ]
    

    shape = arc([-1, 0], [1, 0], 1, subDivs=8)
    del shape[-1]
    shape.extend(arc([1, 0], [3, 0], -1, subDivs=8))
    del shape[-1]
    shape.extend(arc([3, 0], [-3, 0], -1, subDivs=16))
    del shape[-1]
    shape.extend(arc([-3, 0], [-1, 0], -1, subDivs=8))
    del shape[-1]
    
    line = Ribbon(shape, grid, True, 4)

    toDraw = line.getLines()

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
            (round(200 + stroke[0][0] * 50),
             round(200 + -stroke[0][1] * 50)),
            (round(200 + stroke[1][0] * 50),
             round(200 + -stroke[1][1] * 50)))

    pygame.display.update()
    exited = False
    while not exited:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exited = True


main()
