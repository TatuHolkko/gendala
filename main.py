from math import pi
import random
from feature import Feature
from layer import Layer
from generator.generator import Generator
from generator.patternGenerators import crossedBox, topAndBottom, verticalLine
from geometry import Point
from curve import Curve
from display import Display
from ribbon import Ribbon

disp = Display(1200,1000)

def main():

    arcCurve = Curve(Point(-1,0))
    arcCurve.extend(arcCurve.arc(Point(1,0), amplitude=1, subDivs=1))

    xAxisCurve = Curve(Point(-1,0))
    xAxisCurve.extend(xAxisCurve.arc(Point(1,0), amplitude=0, subDivs=1))

    pat = Ribbon(arcCurve, topAndBottom(), closed=False).getPattern(0)
    pat.normalizeX()
    pat.combine(verticalLine(-1))
    pat.combine(verticalLine(1))

    disp.setAutoFlush(True)
    disp.drawDebugGrid()

    if True:
        Layer(0.5,0.2, pat, repeats=2).render(display=disp)
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
