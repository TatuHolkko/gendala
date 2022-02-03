from math import pi
import random
from feature import Feature
from layer import Layer
from generator.generator import Generator
from generator.patternGenerators import horizontalLine, topAndBottom, verticalLine
from geometry import Point
from curve import Curve
from display import Display
from ribbon import Ribbon

disp = Display(1200,1000)

random.seed()

def debugRender():
    arcCurve = Curve(Point(0,0))
    arcCurve.extend(arcCurve.arc(Point(1,0), amplitude=1, subDivs=1))

    feature = Feature()
    feature.add(Ribbon(arcCurve, horizontalLine(0), closed=False))
    
    Layer(1,0.5, feature.getPattern(0.1), repeats=4).render(disp)

def layers():
    s = 0.1
    layers = 5
    r0 = 0.01
    w0 = 0.1

    for i in range(layers):
        w = w0 - 0.01
        r = r0 + w + w0
        pat = Generator().getFeature().getPattern(s)
        l = Layer(r,w*((i%2)*2 - 1), pat, repeats=4+2**(i))
        l.render(disp)
        r0 = r
        w0 = w

def main():
    disp.setAutoFlush(True)
    disp.drawDebugGrid()

    if 0:
        debugRender()
    else:
       layers()
    
    disp.eventLoop()


main()
