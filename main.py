import pygame
from riblet import Riblet
from geospace import GeoSpace


def main():
    pygame.init()
    pygame.display.set_caption("Fractal curve generator")
    surf = pygame.display.set_mode(size=(200, 200))

    extension = [
        [[-1, 1], [0, 1]],
        [[0, 1], [1, 1]],
        [[-1, -1], [0, -1]],
        [[0, -1], [1, -1]],
        [[0, 1], [0, -1]]
    ]

    geospace = GeoSpace(shrinkPoint=(1, 2))

    line = Riblet(geospace)

    toDraw = line.getExtended(extension, 1)

    for stroke in toDraw:
        pygame.draw.line(
            surf,
            (255,
             255,
             255),
            (100 + stroke[0][0] * 50,
             100 + -stroke[0][1] * 50),
            (100 + stroke[1][0] * 50,
             100 + -stroke[1][1] * 50))
    pygame.display.update()
    exited = False
    while not exited:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exited = True


main()
