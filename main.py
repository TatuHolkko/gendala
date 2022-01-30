from dis import dis
from math import pi
from xmlrpc.client import TRANSPORT_ERROR
from feature import Feature
from layer import Layer
from ribbon import Ribbon
from geometry import Point
from curve import Curve
from display import Display

disp = Display(1200,1000)

def main():
    
    diagonalCurve = Curve(Point(-1,0),False)
    diagonalCurve.extend(diagonalCurve.sine(Point(1,0), amplitude=1, subDivs=15))

    
    xAxisCurve = Curve(Point(-1,0))
    xAxisCurve.extend(xAxisCurve.sine(Point(1,0), amplitude=0.1, subDivs=7))

    ribbon = Ribbon(xAxisCurve, diagonalCurve.getPattern(), closed=False)

    feature = Feature(mirrorX=True, mirrorY=True)
    feature.add(ribbon)

    s = 1
    layers = 2
    r0 = 0.5
    w0 = 0.1
    disp.setAutoFlush(True)
    disp.drawDebugGrid()
    #feature.render(disp, 1)
    for i in range(layers):
        w = w0 - 0.01
        r = r0 + w + w0
        l = Layer(r,w*((i%2)*2 - 1),feature.getPattern(s), repeats=4*(i+1))
        l.render(disp)
        r0 = r
        w0 = w
    disp.eventLoop()


main()
