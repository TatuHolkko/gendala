from math import pi
from feature import Feature
from layer import Layer
from ribbon import Ribbon
from geometry import Point
from curve import Curve
from display import Display

disp = Display(1200,1000)

def main():
    
    diagonalCurve = Curve(Point(-1,0),closed=True)
    diagonalCurve.extend(diagonalCurve.arc(Point(1,0), amplitude=-1, subDivs=2))
    diagonalCurve.extend(diagonalCurve.arc(Point(-1,0), amplitude=-1, subDivs=1))
    
    #diagonalCurve.round()

    xAxisCurve = Curve(Point(-1,0))
    xAxisCurve.extend(xAxisCurve.arc(Point(1,0), amplitude=0, subDivs=1))

    ribbon = Ribbon(xAxisCurve, diagonalCurve.getPattern(), closed=False, taperLength=0, n=3)

    feature = Feature(mirrorX=False, mirrorY=True)
    feature.add(ribbon)

    disp.setAutoFlush(True)
    disp.drawDebugGrid()
    if False:
        feature.render(disp, 0.2)
    else:
        s = 1
        layers = 5
        r0 = 0.1
        w0 = 0.1

        for i in range(layers):
            w = w0 - 0.01
            r = r0 + w + w0
            l = Layer(r,w*((i%2)*2 - 1),feature.getPattern(s), repeats=2**(i+1))
            l.render(disp)
            r0 = r
            w0 = w
    disp.eventLoop()


main()
