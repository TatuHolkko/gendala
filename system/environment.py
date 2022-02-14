import os                                           # nopep8
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # nopep8
import pygame                                       # nopep8
import uuid
from common.settings import Settings
import random
import threading
from geometry.point import Point
from hierarchy.curve import Curve
from hierarchy.ribbon import Ribbon
from generation.layer import LayerGenerator
from system.display import Display


class Event():
    def __init__(self) -> None:
        self.queued = False
        self.active = False


class Environment():
    """
    Environment controls the user input and rendering control
    """

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the environment

        Args:
            settings (Settings):  Settings object
        """
        pygame.init()
        pygame.display.set_caption("Gendala")
        self.settings = settings
        self.surf = pygame.display.set_mode(
            size=settings.getList("System", "resolution", int)
        )
        self.display = Display(self.surf, settings=settings)
        self.renderThread = None
        self.debugActive = settings.getBool("Program", "debug")
        self.exited = False
        self.renderingEvent = Event()
        self.saveEvent = Event()
        self.restartEvent = Event()

    def debugRender(self) -> None:
        """
        Drawign function for debugging
        """
        self.display.setColor(255, 0, 0)
        self.display.drawDebugGrid()
        self.display.setColor(255, 255, 255)
        closed = False

        arcCurve = Curve(Point(-1, 0), closed=closed)
        arcCurve.extend(
            arcCurve.arc(
                Point(
                    0.99, -0.5), amplitude=0, subDivs=2000))
        #arcCurve.extend(arcCurve.arc(Point(-1, 0), amplitude=1, subDivs=1))

        lineCurve = Curve(Point(-1, 0), closed=False)
        lineCurve.extend(lineCurve.line(Point(1, 0), subDivs=1))
        r = Ribbon(
            lineCurve,
            arcCurve.getPattern(),
            closed=closed,
            width=1,
            n=1)
        # r.unCollideWidth()
        r.render(self.display)
        #feature = Feature()
        # feature.add(r)
        # feature.render(self.display)

        #Layer(1, 0.5, feature.getPattern(), repeats=4).render(self.display)

    def layers(self) -> None:
        """
        Generate and render a set of layers
        """
        self.display.setColor(0, 0, 0)
        layers = 12
        r0 = 0.02
        w0 = 0.08
        wp = 0
        g = LayerGenerator(self.settings)
        for i in range(layers):
            w = w0 + random.random() * 0.06 - 0.03
            r = r0 + wp + w
            n = random.randint(1, 4)
            repeats = (i + 1) * 4 + n * int(i / 2)
            if self.restartEvent.active:
                break

            l = g.getLayer(radius=r, width=w)

            if self.restartEvent.active:
                break

            l.render(self.display)

            self.display.flushBuffer()

            r0 = r
            wp = w

    def generateRenderFunction(
            self,
            renderFunction: callable[[], None]) -> callable[[], None]:
        """
        Generate a function for rendering thread.

        Args:
            renderFunction (callable[[], None]): function that renders everything

        Returns:
            callable[[], None]: a function to be given for the rendering thread
        """
        def rend():
            self.renderingEvent.active = True
            if self.debugActive:
                self.display.clear()
            else:
                self.display.gradient()
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
                            thread = threading.Thread(
                                target=self.restartRender)
                            thread.start()

                    elif event.key == pygame.K_s:
                        if not self.saveEvent.queued:
                            self.saveEvent.queued = True
