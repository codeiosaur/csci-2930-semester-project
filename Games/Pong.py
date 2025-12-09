from Games.BaseGame import BaseGame as Game, pygame

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

    def on_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, self.white, self.paddle1)
        pygame.draw.rect(self.screen, self.white, self.paddle2)
        pygame.draw.rect(self.screen, self.white, self.ball)