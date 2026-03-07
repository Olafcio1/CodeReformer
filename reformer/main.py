import pygame_ns as _
import pygame

from .resources import ResourceManager

from .lib.screen.Screen import Screen
from .lib.static.StaticRendering import StaticRendering

from .app.home.HomeScreen import HomeScreen

class Rendering:
    surface: pygame.Surface
    screen: Screen

    def __init__(self):
        self.setup_window()

        ResourceManager.loadBuiltin()

        def setter(value):
            self.screen = value

        StaticRendering.getScreen = lambda: self.screen
        StaticRendering.setScreen = setter

        self.surface = pygame.display.get_surface()
        self.screen = HomeScreen()

        self.mainloop()

    def render(self):
        if self.screen.pendingRerender():
            self.screen.render(self.surface)
        else:
            self.screen.renderChanged(self.surface)

    def setup_window(self):
        pygame.init()

        pygame.display.set_caption("Code Reformer")
        pygame.display.set_mode((800, 600))

    def mainloop(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.ACTIVEEVENT:
                self.render()
            elif event.type == pygame.QUIT:
                break
            ### KEYBOARD ###
            elif event.type == pygame.KEYDOWN:
                self.screen.keyPressed(event.key, event.unicode)
                self.render()
            elif event.type == pygame.KEYUP:
                self.screen.keyReleased(event.key, event.unicode)
                self.render()
            ### MOUSE ###
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                self.screen.mousePressed(x, y, event.button)
                self.render()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                self.screen.mouseReleased(x, y, event.button)
                self.render()
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                self.screen.mouseMoved(x, y)
                self.render()

Rendering()
