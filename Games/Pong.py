from Games.BaseGame import BaseGame as Game, pygame
import random

class Pong(Game):
    def __init__(self, screen):
        super().__init__(screen)
        # Other constants
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.run()

    def setup(self):
        self.screen.fill(self.BLACK)
        # Score
        self.score = 0
        # Paddle definition
        self.paddleDims = (20, 200)  # Default paddle width/height; used for collisions
        self.paddleSpeed = int(0.02 * self.screenInfo["height"]) # max paddle speed
        self.paddleVelocity = [0, 0] # How fast is the player moving the paddles?
        self.paddle1 = pygame.Rect(0.1 * self.screenInfo["width"],
                                   0.375 * self.screenInfo["height"],
                                   self.paddleDims[0], self.paddleDims[1])
        self.paddle2 = pygame.Rect(0.9 * self.screenInfo["width"],
                                   0.375 * self.screenInfo["height"],
                                   self.paddleDims[0], self.paddleDims[1])
        # Ball definition
        self.ballDims = (20, 20)  # Default ball radius; used for collisions
        self.ballBaseSpeed = 0.01 * self.screenInfo["height"]
        self.ballSpeed = [self.ballBaseSpeed, self.ballBaseSpeed]
        self.ball = pygame.Rect(0.5 * self.screenInfo["width"],
                                0.5 * self.screenInfo["height"],
                                self.ballDims[0], self.ballDims[1])
        # Make the ball fly off in random direction each time at game start
        if random.random() < 0.5:
            self.ballSpeed[0] *= -1
        if random.random() < 0.5:
            self.ballSpeed[1] *= -1
        # Scaling
        self.paddle1.scale_by_ip(self.screenInfo["scaleX"], self.screenInfo["scaleY"])
        self.paddle2.scale_by_ip(self.screenInfo["scaleX"], self.screenInfo["scaleY"])
        self.ball.scale_by_ip(self.screenInfo["scaleX"], self.screenInfo["scaleY"])

    # Does nothing but required for BaseGame inheritance declaration.
    def on_event(self, event):
        pass

    def on_key(self, keys):
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.paddle1.move_ip(0, -self.paddleSpeed)
            self.paddleVelocity[0] = -self.paddleSpeed
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.paddle1.move_ip(0, self.paddleSpeed)
            self.paddleVelocity[0] = self.paddleSpeed
        else:
            self.paddleVelocity[0] = 0
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.paddle2.move_ip(0, -self.paddleSpeed)
            self.paddleVelocity[1] = -self.paddleSpeed
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.paddle2.move_ip(0, self.paddleSpeed)
            self.paddleVelocity[1] = -self.paddleSpeed
        else:
            self.paddleVelocity[1] = 0

    def update(self):
        paddles = [self.paddle1, self.paddle2]
        height = self.screenInfo["height"]
        # Move ball
        self.ball.move_ip(self.ballSpeed[0], self.ballSpeed[1])
        # Ball collision
        # Is the ball touching the left/right edge?
        if self.ball.left < 0 or self.ball.right > self.screenInfo["width"]:
            self.running = False # end the game
        # Is the ball touching the top/bottom edge?
        if self.ball.top < 0:
            self.ball.top = 0
            self.ballSpeed[1] *= -1
        if self.ball.bottom > height:
            self.ball.bottom = height
            self.ballSpeed[1] *= -1
        # Is the ball touching one of the paddles?
        if self.ball.colliderect(self.paddle1) and self.ballSpeed[0] < 0:
            self.ballSpeed[0] *= -1; self.score += 1
            # Change angle based on hit position
            ballHitPos = (self.ball.centery - self.paddle1.top) / self.paddle1.height
            self.ballSpeed[1] = (int((ballHitPos - 0.5) * 1.2 * self.ballBaseSpeed)
                                 + random.uniform(-0.5, 0.5))
            # paddle momemtum
            self.ballSpeed[1] += int(self.paddleVelocity[0] * 0.3)

        elif self.ball.colliderect(self.paddle2) and self.ballSpeed[0] > 0:
            self.ballSpeed[0] *= -1; self.score += 1
            # Change angle based on hit position
            ballHitPos = (self.ball.centery - self.paddle2.top) / self.paddle2.height
            self.ballSpeed[1] = (int((ballHitPos - 0.5) * 2.4 * self.ballBaseSpeed)
                                 + random.uniform(-0.5, 0.5))
            # paddle momentum
            self.ballSpeed[1] += int(self.paddleVelocity[1] * 0.3)

        # Anti-out of bounds paddle collision logic
        # (are the paddles touching the screen edges?)
        for paddle in paddles:
            if paddle.top < 0: paddle.top = 0
            if paddle.bottom > height:
                paddle.bottom = height

    def draw(self):
        self.screen.fill(self.BLACK)
        pygame.draw.rect(self.screen, self.WHITE, self.paddle1)
        pygame.draw.rect(self.screen, self.WHITE, self.paddle2)
        pygame.draw.rect(self.screen, self.WHITE, self.ball)