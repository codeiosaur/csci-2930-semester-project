from abc import ABC, abstractmethod
import pygame

class BaseGame(ABC):
    def __init__(self, screen, scale_x, scale_y):
        self.screen = screen
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.running = False
        self.clock = pygame.time.Clock()

    def run(self):
        self.running = True
        self.setup()  # Initialize game-specific stuff

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
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

    # Handle game-specific events.
    @abstractmethod
    def on_event(self, event):
        pass

    # Update game logic (aka game loop).
    @abstractmethod
    def update(self):
        pass

    # Render the game.
    @abstractmethod
    def draw(self):
        pass