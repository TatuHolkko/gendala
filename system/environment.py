import os                                           # nopep8
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # nopep8
import pygame                                       # nopep8
import uuid
import random
import threading
from geometry.point import Point
from hierarchy.curve import Curve
from hierarchy.ribbon import Ribbon
from hierarchy.layer import Layer
from hierarchy.feature import Feature
from generation.pattern import box, centerLine, crossedBox, horizontalLine, topAndBottom
from generation.generator import Generator
from system.display import Display

class Event():
    def __init__(self) -> None:
        self.queued = False
        self.active = False

class Environment():
    """
    Environment controls the user input and rendering control
    """
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Gendala")
        self.surf = pygame.display.set_mode(size=(1000, 1000))
        self.display = Display(self.surf, autoFlush=True)
        self.renderThread = None
        self.debugActive = False
        self.exited = False
        self.renderingEvent = Event()
        self.saveEvent = Event()
        self.restartEvent = Event()

    def debugRender(self):
        """
        Drawign function for debugging
        """
        self.display.drawDebugGrid()
        closed = False
        arcCurve = Curve(Point(-1, 0), closed=closed)
        arcCurve.extend(arcCurve.arc(Point(1, 0), amplitude=0, subDivs=1))
        #arcCurve.extend(arcCurve.arc(Point(-1, 0), amplitude=1, subDivs=1))

        r = Ribbon(
            arcCurve,
            centerLine(),
            closed=closed,
            width=0.3,
            n=4)
        #r.unCollideWidth()
        r.render(self.display)
        #feature = Feature()
        #feature.add(r)
        #feature.render(self.display)

        #Layer(1, 0.5, feature.getPattern(), repeats=4).render(self.display)

    def layers(self):
        """
        Generate and render a set of layers
        """
        layers = 12
        r0 = 0.02
        w0 = 0.08
        wp = 0
        g = Generator()
        for i in range(layers):
            w = w0 + random.random() * 0.06 - 0.03
            width = w * ((i % 2) * 2 - 1)
            g.setScale(w)
            pat = g.getFeature().getPattern()

            if self.restartEvent.active:
                break

            n = random.randint(1, 4)
            repeats = (i + 1) * 4 + n * int(i / 2)


            r = r0 + wp + w
            l = Layer(r, width, pat, repeats=repeats)

            if self.restartEvent.active:
                break

            l.render(self.display)

            if self.restartEvent.active:
                break

            r0 = r
            wp = w

    def generateRenderFunction(self, renderFunction):
        """
        Generate a function for rendering thread

        Args:
            renderFunction (function): function that renders everything
        
        Return:
            function: a function to be given for the rendering thread
        """
        def rend():
            self.renderingEvent.active = True
            self.display.clear()
            renderFunction()
            self.renderingEvent.active = False

        return rend

    def startRender(self):
        """
        Start the rendering thread
        """
        if self.debugActive:
            self.renderThread = threading.Thread(
                target=self.generateRenderFunction(
                    self.debugRender))
        else:
            self.renderThread = threading.Thread(
                target=self.generateRenderFunction(self.layers))

        self.renderThread.start()

    def run(self):
        """
        Start the event loop
        """
        self.startRender()
        self.eventLoop()

    def debug(self):
        """
        Start the event loop with debug rendering
        """
        self.debugActive = True
        self.run()

    def restartRender(self):
        """
        Clear the screen and start rendering a new set of layers
        """
        self.restartEvent.queued = True
        self.restartEvent.active = True
        self.display.disableRender()
        self.renderThread.join()
        if not self.exited:
            self.restartEvent.active = False
            self.display.enableRender()
            self.saveEvent.queued = False
            self.startRender()
            self.restartEvent.queued = False

    def eventLoop(self):
        """
        Blocking event loop
        """
        while not self.exited:

            if self.saveEvent.queued and not self.saveEvent.active and not self.renderingEvent.active:
                self.saveEvent.active = True
                pygame.image.save(self.surf,
                                  "../results/" + str(uuid.uuid4()) + ".png")
                self.saveEvent.active = False
                self.saveEvent.queued = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.exited = True
                    self.restartEvent.active = True
                    self.display.disableRender()
                    break

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        if not self.restartEvent.queued:
                            thread = threading.Thread(target=self.restartRender)
                            thread.start()

                    elif event.key == pygame.K_s:
                        if not self.saveEvent.queued:
                            self.saveEvent.queued = True
