import random
import threading
from math import pi
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
    layers = 12
    r0 = 0.001
    w0 = 0.08
    for i in range(layers):
        w = w0
        r = r0 + w + w0
        
        pat = Generator().getFeature().getPattern()
        
        n = random.randint(1,4)
        repeats = (i+1)*4 + n*int(i/4)

        l = Layer(r,w*((i%2)*2 - 1), pat, repeats=repeats)
        l.render(disp)

        r0 = r
        w0 = w

def main():
    disp.setAutoFlush(True)
    #disp.drawDebugGrid()

    if 0:
        debugRender()
    else:
        renderThread = threading.Thread(target=layers, daemon=True)
        renderThread.start()
    
    disp.eventLoop()


main()
