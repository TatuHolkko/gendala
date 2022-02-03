import os                                           # nopep8
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # nopep8
import pygame                                       # nopep8
import random
import threading
from curve import Curve
from feature import Feature
from generator.generator import Generator
from generator.patternGenerators import horizontalLine
from geometry import Point
from layer import Layer
from ribbon import Ribbon

from display import Display


class Environment():

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Gendala")
        self.surf = pygame.display.set_mode(size=(1000, 1000))
        self.display = Display(self.surf)
        self.display.setAutoFlush(True)

    def debugRender(self):
        arcCurve = Curve(Point(0, 0))
        arcCurve.extend(arcCurve.arc(Point(1, 0), amplitude=1, subDivs=1))

        feature = Feature()
        feature.add(Ribbon(arcCurve, horizontalLine(0), closed=False, width=0.1))

        Layer(1, 0.5, feature.getPattern(), repeats=4).render(self.display)

    def layers(self):
        layers = 12
        r0 = 0.001
        w0 = 0.08
        for i in range(layers):
            w = w0
            r = r0 + w + w0

            pat = Generator().getFeature().getPattern()

            n = random.randint(1, 4)
            repeats = (i + 1) * 4 + n * int(i / 4)

            l = Layer(r, w * ((i % 2) * 2 - 1), pat, repeats=repeats)
            l.render(self.display)

            r0 = r
            w0 = w

    def run(self, debug=False):

        if debug:
            self.display.drawDebugGrid()
            renderThread = threading.Thread(target=self.debugRender, daemon=True)
            renderThread.start()
        else:
            renderThread = threading.Thread(target=self.layers, daemon=True)
            renderThread.start()

        self.display.eventLoop()
    
    def debug(self):
        self.run(debug=True)