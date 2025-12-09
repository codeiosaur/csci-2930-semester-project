from math import floor

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
        self.paddleDims = (20, 200) # Default paddle width/height; used for collisions
        self.ballDims = (20, 20) # Default ball radius; used for collisions
        self.paddle1 = pygame.Rect(0.1 * self.screenInfo["width"],
                                   0.375 * self.screenInfo["height"],
                                   self.paddleDims[0], self.paddleDims[1])
        self.paddle2 = pygame.Rect(0.9 * self.screenInfo["width"],
                                   0.375 * self.screenInfo["height"],
                                   self.paddleDims[0], self.paddleDims[1])
        self.ball = pygame.Rect(0.5 * self.screenInfo["width"],
                                0.5 * self.screenInfo["height"],
                                self.ballDims[0], self.ballDims[1])
        # Scaling
        self.paddle1.scale_by_ip(self.screenInfo["scaleX"], self.screenInfo["scaleY"])
        self.paddle2.scale_by_ip(self.screenInfo["scaleX"], self.screenInfo["scaleY"])
        self.ball.scale_by_ip(self.screenInfo["scaleX"], self.screenInfo["scaleY"])

    # Does nothing but required
    # for BaseGame inheritance declaration.
    def on_event(self, event):
        pass

    def on_key(self, keys):
        paddleSpeed = int(0.01 * self.screenInfo["height"])
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.paddle1.move_ip(0, -paddleSpeed)
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.paddle1.move_ip(0, paddleSpeed)
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.paddle2.move_ip(0, -paddleSpeed)
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.paddle2.move_ip(0, paddleSpeed)

    def update(self):
        # Anti-out of bounds collision logic
        # (are the paddles touching the screen?)
        paddles = [self.paddle1, self.paddle2]
        height = self.screenInfo["height"]
        for paddle in paddles:
            if paddle.top < 0: paddle.top = 0
            if paddle.bottom > height:
                paddle.bottom = height

    def draw(self):
        self.screen.fill(self.black)
        # print(f"Drawing paddle1 at: {self.paddle1}")
        pygame.draw.rect(self.screen, self.white, self.paddle1)
        pygame.draw.rect(self.screen, self.white, self.paddle2)
        pygame.draw.rect(self.screen, self.white, self.ball)

        # pygame.draw.rect(self.screen, (255, 0, 0), self.paddle1, 2)  # Red outline
        # pygame.draw.line(self.screen, (0, 255, 0),
        #                  (0, self.screenInfo["height"] - 1),
        #                  (self.screenInfo["width"], self.screenInfo["height"] - 1), 2)