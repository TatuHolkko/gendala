import os                                           # nopep8
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # nopep8
import pygame                                       # nopep8
import uuid
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
        self.renderThread = False
        self.haltRender = False
        self.renderingDone = False
        self.saveQueued = False
        self.debugActive = False
        self.exited = False

    def debugRender(self):
        arcCurve = Curve(Point(0, 0))
        arcCurve.extend(arcCurve.arc(Point(1, 0), amplitude=1, subDivs=1))

        feature = Feature()
        feature.add(
            Ribbon(
                arcCurve,
                horizontalLine(0),
                closed=False,
                width=0.1))

        Layer(1, 0.5, feature.getPattern(), repeats=4).render(self.display)

    def layers(self):
        layers = 12
        r0 = 0.001
        w0 = 0.08
        for i in range(layers):
            w = w0
            r = r0 + w + w0

            pat = Generator().getFeature().getPattern()

            if self.haltRender:
                break

            n = random.randint(1, 4)
            repeats = (i + 1) * 4 + n * int(i / 4)

            l = Layer(r, w * ((i % 2) * 2 - 1), pat, repeats=repeats)

            if self.haltRender:
                break

            l.render(self.display)

            if self.haltRender:
                break

            r0 = r
            w0 = w

    def generateRenderFunction(self, renderFunction):

        def rend():
            self.renderingDone = False
            renderFunction()
            self.renderingDone = True

        return rend

    def startRender(self):

        self.display.clear()

        if self.debugActive:
            self.display.drawDebugGrid()
            self.renderThread = threading.Thread(
                target=self.generateRenderFunction(
                    self.debugRender))
        else:
            self.renderThread = threading.Thread(
                target=self.generateRenderFunction(self.layers))

        self.renderThread.start()

    def run(self):
        self.startRender()
        self.eventLoop()

    def debug(self):
        self.debugActive = True
        self.run()
    
    def restartRender(self):
        self.haltRender = True
        self.display.disableRender()
        self.renderThread.join()
        if not self.exited:
            self.haltRender = False
            self.display.enableRender()
            self.saveQueued = False
            self.startRender()

    def eventLoop(self):
        
        while not self.exited:

            if self.saveQueued and self.renderingDone:
                pygame.image.save(self.surf,
                                  "results/" + str(uuid.uuid4()) + ".png")
                self.saveQueued = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.exited = True
                    self.haltRender = True
                    self.display.disableRender()
                    break

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        thread = threading.Thread(target=self.restartRender)
                        thread.start()

                    elif event.key == pygame.K_s:
                        self.saveQueued = True
