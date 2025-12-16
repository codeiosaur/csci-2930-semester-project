#error from menus import perplexity is confused

import pygame
import random
from BaseGame import BaseGame as Game
from Menus.utils import draw_text as drawText, userId
from Data.DatabaseManager import DatabaseManager
from time import time

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

resultColors = [black, darkGrey, lightGrey]

radius = 2.5

class Mastermind(Game):
    def __init__(self, screen):
        super().__init__(screen)
        self.answers = []
        self.answerSurfaces = []
        self.plays = []
        self.playSurfaces = []
        self.current = []
        self.currentSurfaces = []
        self.key = []
        self.setKey()
        self.index = 0
        self.win = False
        self.point = True
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
            anSurRow = []
            playRow = []
            playSurRow = []
            for column in range(5):
                answerRow.append(white)
                anSurRow.append(self.createButton(screen, white, [column * (self.SCREEN_WIDTH / 7) + 5, row * (self.SCREEN_HEIGHT / 14) + 5], radius))
                playRow.append(white)
                playSurRow.append(self.createButton(screen, white, [(self.SCREEN_WIDTH / 2) + column * (self.SCREEN_WIDTH / 7) + 5, row * (self.SCREEN_HEIGHT / 14) + 5], radius))
            self.answers.append(answerRow)
            self.plays.append(playRow)
        for column in range(len(playColors)):
            self.current.append(playColors[column])
            self.currentSurfaces.append(self.createButton(screen, playColors[column], [5 + (self.SCREEN_WIDTH / 2) + column * (self.SCREEN_WIDTH/7), self.SCREEN_HEIGHT - 5], radius))
        self.submit = pygame.Rect(0, self.SCREEN_HEIGHT - 15, self.SCREEN_WIDTH / 4, 50, 10)
        pygame.draw.rect(0, self.SCREEN_HEIGHT - 15, self.SCREEN_WIDTH / 4, 50, 10)
        drawText(screen, "Submit", ("menlo", 45), black, 0, self.SCREEN_HEIGHT - 15)
        self.startTime = time()

    def getColor(self, position):
        return self.screen.get_at(position)[:3] 

    def isIn(self, object, position):
        return object.collidepoint(position)  

    def on_event(self): #Fix collide point surfaces
        while self.win == False and self.index < 12:
            if pygame.mouse.get_pressed():
                position = pygame.mouse.get_pos()
                if self.isIn(self.submit, position):
                    filled = True
                    for button in self.plays[self.index]:
                        if self.getColor(position) == white:
                            filled = False
                            break
                    if filled:
                        self.submit()
                for button in range(8):
                    if self.isIn(self.playSurfaces[self.index][button], position) and self.getColor(position) != white:
                        self.remove(self.getColor(position), button)
                for button in range(len(self.current)):
                    if self.isIn(self.currentSurfaces[button], position) and self.getColor(position) != white:
                        self.add(self.getColor(position), button)
        self.endTime = time()
        self.scoring()

    def getRectPos(self, rect):
        return [rect.x, rect.y, rect.width, rect.height]
    
    def getCircPos(self, circ):
        return ((circ.x + (circ.width / 2), circ.y + (circ.height / 2)))
    
    def add(self, color, button):
        for button in range(5):
            position = self.getCircPos(self.playSurfaces[self.index][button])
            if self.getColor(position) == white:
                self.drawButton(self.screen, color, position, radius)
                self.plays[self.index][button] = color
                for saved in range(len(playColors)):
                    if playColors[saved] == color:
                        self.drawButton(self.screen, white, self.getCircPos(self.currentSurfaces[saved]), radius)
                        self.current[saved] = white
                        break
                break

    def remove(self, color, index):
        self.plays[self.index][index] = white
        position = self.getCircPos(self.playSurfaces[self.index][index])
        self.drawButton(self.screen, white, position, radius)
        for saved in range(len(playColors)):
            if color == playColors[saved]:
                self.current[saved] = color
                position = (self.getCircPos(self.currentSurfaces[saved]))
                self.drawButton(self.screen, color, position, radius)
                break

    def submit(self):
        result = [0, 0, 0]
        for index in range(5):
            if self.current[index] == self.key[index]:
                result[0] += 1
            elif self.current[index] in self.key:
                result[1] += 1
            else:
                result[2] += 1
        if result[0] == 5:
            self.win = True
        loopindex = 0
        for res in len(result):
            for ind in range(result[res]):
                self.answers[self.index][ind] = resultColors[res]
                self.drawButton(self.screen, resultColors[res], self.getCircPos(self.answerSurfaces[self.index][loopindex]), radius)
                loopindex += 1
        self.plays[self.index] = self.current
        for index in range(5):
            self.drawButton(self.screen, self.plays[self.index][index], self.getCircPos(self.playSurfaces[self.index][index]), radius)
        self.current = playColors
        for index in range(len(8)):
            self.drawButton(self.screen, self.current[index], self.getCircPos(self.currentSurfaces[index]), radius)
        self.index += 1

    def scoring(self):
        colorPoint = 0
        for row in self.answers:
            for color in row:
                if color == black:
                    colorPoints += 5
                elif color == darkGrey:
                    colorPoints = 2
        score = (12-self.index) * 10 + colorPoints
        if userId != None:
            db = DatabaseManager()
            db.endGame(self.point, score, userId,"Mastermind", self.endTime - self.startTime)

    def on_key(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass