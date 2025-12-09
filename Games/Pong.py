from Games.BaseGame import BaseGame as Game, pygame
import random

class Pong(Game):
    def __init__(self, screen):
        super().__init__(screen)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.run()

    def setup(self):
        self.screen.fill(self.black)
        self.paddle1 = pygame.Rect(100 * self.screenInfo["scaleX"],
                                   300 * self.screenInfo["scaleY"],
                                   20 * self.screenInfo["scaleX"],
                                   200 * self.screenInfo["scaleY"])
        self.paddle2 = pygame.Rect(900 * self.screenInfo["scaleX"],
                                   300 * self.screenInfo["scaleY"],
                                   20 * self.screenInfo["scaleX"],
                                   200 * self.screenInfo["scaleY"])
        self.ball = pygame.Rect(500 * self.screenInfo["scaleX"],
                                400 * self.screenInfo["scaleY"],
                                20 * self.screenInfo["scaleX"],
                                20 * self.screenInfo["scaleY"])

    def on_key(self, keys):
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.paddle1.move_ip(0, -5)
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.paddle1.move_ip(0, 5)
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.paddle2.move_ip(0, -5)
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.paddle2.move_ip(0, 5)

    def update(self):
        self.screen.fill(self.black)

    def draw(self):
        pygame.draw.rect(self.screen, self.white, self.paddle1)
        pygame.draw.rect(self.screen, self.white, self.paddle2)
        pygame.draw.rect(self.screen, self.white, self.ball)