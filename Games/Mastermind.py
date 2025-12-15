import pygame
import pygame_widgets as widgets
from Games.BaseGame import BaseGame as Game
from Menus.utils import draw_text as drawText

red = (255, 0, 0)
orange = (255, 255, 0)
yellow = (0, 255, 0)
green = (0, 255, 255)
blue = (0, 0, 255)
purple = (255, 0, 255)

white = (255, 255, 255)
lightGrey = (200, 200, 200)
darkGrey = (100, 100, 100)
black = (0, 0, 0)

class Mastermind(Game):
    def __init__(self, screen):
        super().__init__(screen)
        self.answers = []
        self.plays = []
        self.current = []
        self.run()
    
    def setup(self, screen):
        self.screen.fill(white)
        answerBox = pygame.Rect(0, 0, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT)
        playBox = pygame.Rect(self.SCREEN_WIDTH / 2, 0, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT)
        for row in range(12):
            answerRow = []
            playRow = []
            for column in range(5):
                answerRow.append(pygame.draw.circle(screen, white, [column * (self.SCREEN_WIDTH / 7) + 5, row * (self.SCREEN_HEIGHT / 14) + 5], 2.5))
                playRow.append(pygame.draw.circle(screen, white, [(self.SCREEN_WIDTH / 2) + column * (self.SCREEN_WIDTH / 7) + 5, row * (self.SCREEN_HEIGHT / 14) + 5], 2.5))
            self.answers.append(answerRow)
            self.plays.append(playRow)
        for column in range(8):
            self.current.append(pygame.draw.circle(screen, white, [5 + (self.SCREEN_WIDTH / 2) + column * (self.SCREEN_WIDTH/7), self.SCREEN_HEIGHT - 5], 2.5))
        self.submit = pygame.Rect(0, self.SCREEN_HEIGHT - 15, self.SCREEN_WIDTH / 4)
        drawText(screen, "Submit", ("menlo", 45), black, 0, self.SCREEN_HEIGHT - 15)

    def on_event(self):
        while True:
            if pygame.mouse.get_pressed():
                position = pygame.mouse.get_pos()
                if self.submit.get_rect().collidepoint(position):
                    self.submit()
                for row in self.plays:
                    for button in self.plays:
                        if button.get_rect().collidepoint(position):
                            self.remove()
                for button in self.current:
                    if button.get_rect().collidepoint(position):
                        self.add()

    def add(self):
        pass

    def remove(self):
        pass

    def submit(self):
        pass

    def on_key(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass