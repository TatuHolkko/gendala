import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from ribbon import Ribbon
from geospace import GeoSpace

def main():
    pygame.init()
    pygame.display.set_caption("Fractal curve generator")

    surf = pygame.display.set_mode(size=(400, 400))

    debug_square = [[[-1,1],[1,1]],[[1,1],[1,-1]],[[1,-1],[-1,-1]],[[-1,-1],[-1,1]]]

    extension = [
        [[-1,-1], [1,1]],
        [[-1, 1], [0, 1]],
        [[0, 1], [1, 1]],
        [[-1, -1], [0, -1]],
        [[0, -1], [1, -1]],
        [[0, 1], [0, -1]]
    ]

    shape = [(-1,0), (0,1), (1,0), (0,-1)]

    line = Ribbon(shape, extension, True)

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
