from math import pi
from feature import Feature
from layer import Layer
from ribbon import Ribbon
from utility import Point
from curve import Curve
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

windowSize = 1000

def main():
    pygame.init()
    pygame.display.set_caption("Gendala")

    surf = pygame.display.set_mode(size=(windowSize, windowSize))

    debug_square = [[[-1, 1], [1, 1]], [[1, 1], [1, -1]],
                    [[1, -1], [-1, -1]], [[-1, -1], [-1, 1]]]

    grid = [
        #[[-1, 0], [0, 1]],
        #[[-1, -1], [1, 1]], # diag 1
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
    
    #patternCurve = Curve(Point(-1,-1),False)

    
    patternCurve = Curve(Point(-1,-1),True)
    patternCurve.extend(patternCurve.line(Point(1,-1)))
    patternCurve.extend(patternCurve.sine(Point(1,1), amplitude=-0.5, subDivs=8))
    patternCurve.extend(patternCurve.line(Point(-1,1)))
    patternCurve.extend(patternCurve.sine(Point(-1,-1), amplitude=0.5, subDivs=8))
    #patternCurve.round(pi/2)
    
    featureCurve = Curve(Point(-1,0))
    #featureCurve.extend(featureCurve.arc(Point(1,0), curvature=0))
    #featureCurve.extend(featureCurve.line(Point(1,0)))
    featureCurve.extend(featureCurve.sine(Point(1,0), amplitude=0, subDivs=0))

    ribbon = Ribbon(featureCurve, patternCurve.getLines(), closed=False)

    feature = Feature(mirrorX=True, mirrorY=False)
    feature.add(ribbon)

    s = 1
    toDraw = []
    layers = 8
    r0 = 0.05
    w = 0.1
    for i in range(layers):
        r = r0 + w*2
        w = 0.1 - 0.099999*(i/layers)
        toDraw.extend(Layer(r,w,feature.render(s), repeats=2**(i+1)).render())
        r0 = r

    for stroke in debug_square:
        continue
        pygame.draw.line(
            surf,
            (255,
             0,
             0),
            (round(windowSize/2 + stroke[0][0] * windowSize/3),
             round(windowSize/2 + -stroke[0][1] * windowSize/3)),
            (round(windowSize/2 + stroke[1][0] * windowSize/3),
             round(windowSize/2 + -stroke[1][1] * windowSize/3)))

    for stroke in toDraw:
        pygame.draw.line(
            surf,
            (255,
             255,
             255),
            (round(windowSize/2  + stroke.p0.x * windowSize/3),
             round(windowSize/2  + -stroke.p0.y * windowSize/3)),
            (round(windowSize/2  + stroke.p1.x * windowSize/3),
             round(windowSize/2  + -stroke.p1.y * windowSize/3)))

    pygame.display.update()
    exited = False
    while not exited:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exited = True


main()
