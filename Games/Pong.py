from Games.BaseGame import BaseGame as Game, pygame
from Menus.utils import draw_text as drawText, setPreviousWinner as setWinner
import random

# Used Claude Sonnet for debugging, but 90% of the code is human-written.
# The 10% that isn't is credited as such below.

class Pong(Game):
    def __init__(self, screen):
        super().__init__(screen)
        # Pong-specific constants
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.PADDLE_DIMS = (20, 200)
        self.BALL_DIMS = (20, 20)
        self.BALL_BASE_SPEED = 0.01 * self.SCREEN_HEIGHT
        self.run()

    # Useful because we need to set up the ball when the game starts
    # AND when someone scores (unlike with the paddles.)
    def setupBall(self):
        self.ballSpeed = [self.BALL_BASE_SPEED, self.BALL_BASE_SPEED]
        self.ball = pygame.Rect(0.5 * self.SCREEN_WIDTH,
                                0.5 * self.SCREEN_HEIGHT,
                                self.BALL_DIMS[0], self.BALL_DIMS[1])

    def setup(self):
        self.screen.fill(self.BLACK)
        # Score/winner-related things
        self.score = 0; self.scoreAI = 0
        self.font = pygame.font.SysFont("menlo", 45)
        # Paddle definition
        self.paddleSpeed = int(0.02 * self.SCREEN_HEIGHT) # max paddle speed
        self.paddleVelocity = [0, 0] # How fast is the player moving the paddles?
        self.paddle1 = pygame.Rect(0.1 * self.SCREEN_WIDTH,
                                   0.375 * self.SCREEN_HEIGHT,
                                   self.PADDLE_DIMS[0], self.PADDLE_DIMS[1])
        self.paddle2 = pygame.Rect(0.9 * self.SCREEN_WIDTH,
                                   0.375 * self.SCREEN_HEIGHT,
                                   self.PADDLE_DIMS[0], self.PADDLE_DIMS[1])
        self.paddleCounter = 0 # used for paddle AI
        # Ball definition
        self.setupBall()
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

    def update(self):
        self.paddleCounter += 1
        paddles = [self.paddle1, self.paddle2]
        height = self.SCREEN_HEIGHT
        # Move ball
        self.ball.move_ip(self.ballSpeed[0], self.ballSpeed[1])
        # Move other paddle - but only every other frame.
        # Reduces stuttering.
        if self.paddleCounter % 2 == 0:
            if self.ball.centery - self.paddle2.centery < -10:
                self.paddle2.move_ip(0, int(-self.paddleSpeed * 0.75))
                self.paddleVelocity[1] = int(-self.paddleSpeed * 0.75)
            elif self.ball.centery > self.paddle2.centery:
                self.paddle2.move_ip(0, int(self.paddleSpeed * 0.75))
                self.paddleVelocity[1] = int(self.paddleSpeed * 0.75)
            self.paddleCounter = 0

        # Ball collision
        # Is the ball touching the left/right edge?
        # If so, check to see whether someone won.
        if self.ball.left < 0:
            self.scoreAI += 1
            if self.scoreAI >= 5:
                self.running = False # end the game
                setWinner(False) # player lost
            else:
                self.paddle1.move_ip(0, int(0.375 * self.SCREEN_HEIGHT - self.paddle1.top))
                self.paddle2.move_ip(0, int(0.375 * self.SCREEN_HEIGHT - self.paddle2.top))
                self.paddleVelocity[0] = self.paddleVelocity[1] = 0
                self.setupBall()
        if self.ball.right > self.SCREEN_WIDTH:
            self.score += 1
            if self.score >= 5:
                self.running = False
                setWinner(True) # player won
            else:
                self.paddle1.move_ip(0, int(0.375 * self.SCREEN_HEIGHT - self.paddle1.top))
                self.paddle2.move_ip(0, int(0.375 * self.SCREEN_HEIGHT - self.paddle2.top))
                self.paddleVelocity[0] = self.paddleVelocity[1] = 0
                self.setupBall()
        # Is the ball touching the top/bottom edge?
        if self.ball.top < 0:
            self.ball.top = 0
            self.ballSpeed[1] *= -1
        if self.ball.bottom > height:
            self.ball.bottom = height
            self.ballSpeed[1] *= -1
        # Is the ball touching one of the paddles?
        if self.ball.colliderect(self.paddle1) and self.ballSpeed[0] < 0:
            self.ballSpeed[0] *= -1 + random.uniform(-0.5, 0.5)
            # Normalize x-axis speed
            if abs(self.ballSpeed[0]) < self.BALL_BASE_SPEED:
                if self.ballSpeed[0] > 0:
                    self.ballSpeed[0] = self.BALL_BASE_SPEED
                else:
                    self.ballSpeed[0] = self.BALL_BASE_SPEED
            if abs(self.ballSpeed[0]) > 3 * self.BALL_BASE_SPEED:
                if self.ballSpeed[0] > 0:
                    self.ballSpeed[0] = 3 * self.BALL_BASE_SPEED
                else:
                    self.ballSpeed[0] = 3 * -self.BALL_BASE_SPEED
            # Change angle based on hit position and momentum.
            # Code written by Claude.
            ballHitPos = (self.ball.centery - self.paddle1.top) / self.paddle1.height
            self.ballSpeed[1] = (int((ballHitPos - 0.5) * 2.4 * self.BALL_BASE_SPEED))
            self.ballSpeed[1] += int(self.paddleVelocity[0] * 0.3)

        elif self.ball.colliderect(self.paddle2) and self.ballSpeed[0] > 0:
            self.ballSpeed[0] *= -1 + random.uniform(-0.5, 0.5)
            # Normalize x-axis speed
            if abs(self.ballSpeed[0]) < self.BALL_BASE_SPEED:
                if self.ballSpeed[0] > 0:
                    self.ballSpeed[0] = self.BALL_BASE_SPEED
                else:
                    self.ballSpeed[0] = self.BALL_BASE_SPEED
            if abs(self.ballSpeed[0]) > 3 * self.BALL_BASE_SPEED:
                if self.ballSpeed[0] > 0:
                    self.ballSpeed[0] = 3 * self.BALL_BASE_SPEED
                else:
                    self.ballSpeed[0] = 3 * -self.BALL_BASE_SPEED
            # Change angle based on hit position and momentum.
            # Code written by Claude.
            ballHitPos = (self.ball.centery - self.paddle2.top) / self.paddle2.height
            self.ballSpeed[1] = (int((ballHitPos - 0.5) * 2.4 * self.BALL_BASE_SPEED)
                                 + random.uniform(-0.5, 0.5))
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
        drawText(self.screen, f"{self.score}", self.font, self.WHITE, 400, 100)
        drawText(self.screen, f"{self.scoreAI}", self.font, self.WHITE, 600, 100)