from abc import ABC, abstractmethod
import pygame
from Menus.utils import getScreenDims

class BaseGame(ABC):
    def __init__(self, screen):
        self.screen = screen
        self.screenInfo = getScreenDims()
        self.running = False
        self.clock = pygame.time.Clock()
        self.SCREEN_HEIGHT = self.screenInfo["height"]
        self.SCREEN_WIDTH = self.screenInfo["width"]
        self.point = bool #Set to True if tracking points or False if tracking by time (sec)

    def run(self):
        self.running = True
        self.setup()  # Initialize game-specific things

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        self.on_key(pygame.key.get_pressed())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False  # Return to menu
            self.on_event(event)

    # Initialize the game.
    @abstractmethod
    def setup(self):
        pass

    # Handle game-specific events other than key presses.
    @abstractmethod
    def on_event(self, event):
        pass

    # Handle key presses.
    @abstractmethod
    def on_key(self, keys):
        pass

    # Update game logic (aka game loop).
    @abstractmethod
    def update(self):
        pass

    # Render the game.
    @abstractmethod
    def draw(self):
        pass