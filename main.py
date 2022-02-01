from math import pi
import random
from feature import Feature
from layer import Layer
from generator.generator import Generator
from generator.patternGenerators import crossedBox, verticalLine
from geometry import Point
from curve import Curve
from display import Display
from ribbon import Ribbon

disp = Display(1200,1000)

def main():
    
    diagonalCurve = Curve(Point(-1,0),closed=True)
    diagonalCurve.extend(diagonalCurve.arc(Point(1,0), amplitude=-1, subDivs=2))
    diagonalCurve.extend(diagonalCurve.arc(Point(-1,0), amplitude=-1, subDivs=1))
    
    #diagonalCurve.round()

    xAxisCurve = Curve(Point(-1,0))
    xAxisCurve.extend(xAxisCurve.arc(Point(1,0), amplitude=0, subDivs=1))

    #ribbon = Ribbon(xAxisCurve, diagonalCurve.getPattern(), closed=False, taperLength=0, n=3)


    feature = Generator().getFeature()
    pat = feature.getPattern(0.1)
    pat.combine(verticalLine(1))
    pat.combine(verticalLine(-1))
    #pat.normalizeX()

    disp.setAutoFlush(True)
    disp.drawDebugGrid()
    if False:
        Ribbon(xAxisCurve, pat, closed=False).render(disp, 1)
    else:
        s = 0.1
        layers = 4
        r0 = 0.01
        w0 = 0.1

        for i in range(layers):
            w = w0 - 0.01
            r = r0 + w + w0
            n = random.randint(1,4)
            
            l = Layer(r,w*((i%2)*2 - 1), pat, repeats=8)
            l.render(disp)
            r0 = r
            w0 = w
    disp.eventLoop()


main()
