import pygame
import random
from Games.BaseGame import BaseGame as Game
from Menus.utils import draw_text as drawText

red = (255, 0, 0)
orange = (255, 255, 0)
yellow = (0, 255, 0)
green = (0, 255, 255)
blue = (0, 0, 255)
purple = (255, 0, 255)

playColors = [red, orange, yellow, green, blue, purple]

white = (255, 255, 255)
lightGrey = (200, 200, 200)
darkGrey = (100, 100, 100)
black = (0, 0, 0)

class Mastermind(Game):
    def __init__(self, screen):
        super().__init__(screen)
        self.answers = []
        self.plays = []
        self.playSurfaces = []
        self.current = []
        self.currentSurfaces = []
        self.key = []
        self.setKey()
        self.index = 0
        self.run()
    
    def setKey(self):
        unused = playColors
        while len(self.key) < 5:
            index = int(random.random() * len(unused))
            self.key.append(unused[index])
            unused.pop(index)

    def drawButton(self, screen, color, center, radius):
        pygame.draw.circle(screen, color, center, radius)
    
    def createButton(self, screen, color, center, radius):
        self.drawButton(self, screen, color, center, radius)
        return pygame.Rect(center[0] - radius, center[1] - radius, 2 * radius, 2 * radius)
    
    def setup(self, screen): #fix rectangles behind circles
        self.screen.fill(white)
        pygame.draw.rect(0, 0, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT)
        pygame.draw.rect(self.SCREEN_WIDTH / 2, 0, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT)
        for row in range(12):
            answerRow = []
            playRow = []
            for column in range(5):
                answerRow.append(white)
                pygame.draw.circle(screen, white, [column * (self.SCREEN_WIDTH / 7) + 5, row * (self.SCREEN_HEIGHT / 14) + 5], 2.5)
                playRow.append(white)
                self.playSurfaces.append(self.createButton(screen, white, [(self.SCREEN_WIDTH / 2) + column * (self.SCREEN_WIDTH / 7) + 5, row * (self.SCREEN_HEIGHT / 14) + 5], 2.5))
            self.answers.append(answerRow)
            self.plays.append(playRow)
        for column in range(len(playColors)):
            self.current.append(playColors[column])
            self.currentSurfaces.append(self.createButton(screen, playColors[column], [5 + (self.SCREEN_WIDTH / 2) + column * (self.SCREEN_WIDTH/7), self.SCREEN_HEIGHT - 5], 2.5))
        self.submit = pygame.Rect(0, self.SCREEN_HEIGHT - 15, self.SCREEN_WIDTH / 4, 50, 10)
        pygame.draw.rect(0, self.SCREEN_HEIGHT - 15, self.SCREEN_WIDTH / 4, 50, 10)
        drawText(screen, "Submit", ("menlo", 45), black, 0, self.SCREEN_HEIGHT - 15)

    def getColor(self, position):
        return self.screen.get_at(position)[:3] 

    def isIn(self, object, position):
        return object.collidepoint(position)  

    def on_event(self): #Fix collide point surfaces
        while True: #Fix to ongoing game
            if pygame.mouse.get_pressed():
                position = pygame.mouse.get_pos()
                if self.isIn(self.submit, position):
                    filled = True
                    for button in self.plays[self.index]:
                        if self.getColor == white:
                            filled  = False
                            break
                    if filled:
                        self.submit()
                for button in range(8):
                    if self.isIn(self.playSurfaces[self.index][button], position) and self.getColor(position) != white:
                        self.remove(self.getColor(position), button)
                for button in range(len(self.current)):
                    if self.isIn(self.currentSurfaces[self.index][button], position) and self.getColor(position) != white:
                        self.add(self.getColor(position), button)

    def getRectPos(self, rect):
        return [rect.x, rect.y, rect.width, rect.height]
    
    def getCircPos(self, circ):
        return [(circ.x + (circ.width / 2), circ.y + (circ.height / 2)), circ.width / 2]
    
    def add(self, color, button):
        for button in range(5):
            rect = self.getCircPos(self.playSurfaces[self.index][button])
            position = (rect[0], rect[1])
            if self.getColor(position) == white:
                self.drawButton(self.screen, color, position, 2.5)
                self.plays[self.index][button] = color
                for saved in range(len(playColors)):
                    if playColors[saved] == color:
                        self.drawButton(self.screen, white, self.getCircPos(self.currentSurfaces[saved]), 2.5)
                        self.current[self.index][saved] = white

    def remove(self, color, index):
        pass #set color of plays index to white
        for saved in range(len(playColors)):
            if color == playColors[saved]:
                pass #set index button color to moving color

    def submit(self):
        self.plays = self.current
        #reset current colors
        unused = [0, 1, 2, 3, 4]
        for index in unused:
            pass

    def on_key(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass