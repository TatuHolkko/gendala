from dis import dis
from math import pi
from feature import Feature
from layer import Layer
from ribbon import Ribbon
from utility import Point
from curve import Curve
from display import Display

windowSize = 1000
disp = Display(1200,1000)

def main():

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

    
    diagonalCurve = Curve(Point(-1,-1),False)
    diagonalCurve.extend(diagonalCurve.arc(Point(1,1),curvature=1, subDivs=0))
    #patternCurve = Curve(Point(-1,-1))
    #patternCurve.extend(patternCurve.line(Point(1,-1)))
    #patternCurve.extend(patternCurve.sine(Point(1,1), amplitude=-0.5, subDivs=8))
    #patternCurve.extend(patternCurve.line(Point(-1,1)))
    #patternCurve.extend(patternCurve.sine(Point(-1,-1), amplitude=0.5, subDivs=8))
    #patternCurve.round(pi/2)
    
    xAxisCurve = Curve(Point(-1,0))
    #featureCurve.extend(featureCurve.arc(Point(1,0), curvature=0))
    #featureCurve.extend(featureCurve.line(Point(1,0)))
    xAxisCurve.extend(xAxisCurve.sine(Point(1,0), amplitude=0, subDivs=0))

    ribbon = Ribbon(xAxisCurve, diagonalCurve.getLines(), closed=False)

    feature = Feature(mirrorX=True, mirrorY=True)
    feature.add(ribbon)

    s = 1
    toDraw = []
    layers = 10
    r0 = 0.01
    w0 = 0.15
    disp.setAutoFlush(True)
    disp.drawDebugGrid()
    #feature.render(disp, 1)
    for i in range(layers):
        w = w0 - 0.01
        r = r0 + w + w0
        l = Layer(r,w*((i%2)*2 - 1),feature.getLines(s), repeats=2**(i+1))
        l.render(disp)
        r0 = r
        w0 = w
    disp.eventLoop()


main()
