from Games.BaseGame import BaseGame as Game, pygame
from Menus.utils import draw_text as drawText, scale_rect as scaleRect, setPreviousWinner as setWinner
import random
import math

class Minesweeper(Game):
    CELL_COLORS = [
        (200,200,200),
        (0,0,255),
        (0,128,0),
        (255,0,0),
        (0,0,128),
        (128,0,0),
        (0,128,128),
        (0,0,0),
        (128,128,128)
    ]
    class Cell:
        def __init__(self, pos_x, pos_y, Instance):
            self.is_mine = False
            self.adjacent = 0
            self.revealed = False
            self.flagged = False
            self.x = pos_x
            self.y = pos_y
            self.game = Instance


        def reveal(self):
            self.count_adjacent()
            if not (self.revealed or self.flagged):
                if self.is_mine:
                    self.revealed = True
                    self.game.lose()
                else:
                    self.revealed = True
                    if self.adjacent == 0:
                        self.reveal_adjacent()

        def count_adjacent(self):
            adj = 0
            for i in range(self.x-1,self.x+2):
                for j in range(self.y-1, self.y+2):
                    if 0 <= i < self.game.BOARD_ROWS and 0 <= j < self.game.BOARD_COLS:
                        if self.game.board[i][j].is_mine:
                            adj += 1
            self.adjacent = adj

        def reveal_adjacent(self):
            for i in range(self.x-1,self.x+2):
                for j in range(self.y-1,self.y+2):
                    if 0 <= i < self.game.BOARD_ROWS:
                        if 0 <= j < self.game.BOARD_COLS:
                            self.game.board[i][j].reveal()


        def flag(self):
            if self.flagged:
                self.flagged = False
            else:
                self.flagged = True


    def __init__(self, screen):
        super().__init__(screen)
        # Minesweeper constants here - mines depending on difficulty
        self.BOARD_ROWS = 10
        self.BOARD_COLS = 10
        self.TOTAL_MINES = 10
        self.run()

    # Place the mines in random locations
    def placeMines(self):

        num_mines = 0
        while num_mines < self.TOTAL_MINES:
            x = random.randint(0,self.BOARD_ROWS-1)
            y = random.randint(0,self.BOARD_COLS-1)
            if not self.board[x][y].is_mine:
                self.board[x][y].is_mine = True
                num_mines += 1


    def setup(self):
        self.font = pygame.font.SysFont("arial", 20)
        self.board = [[Minesweeper.Cell(i,j,self) for j in range(self.BOARD_COLS)] for i in range(self.BOARD_ROWS)]
        self.placeMines()


    def revealAll(self):
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                self.board[i][j].reveal()

    def lose(self):
        self.revealMines()


    def win(self):
        pass

    def revealMines(self):
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                if self.board[i][j].is_mine:
                    if self.board[i][j].flagged:
                        self.board[i][j].flag()
                    self.board[i][j].reveal()

    def checkWin(self):
        revealed = 0
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                if self.board[i][j].revealed:
                    revealed += 1
        if revealed == self.BOARD_ROWS * self.BOARD_COLS - self.TOTAL_MINES:
            return True
        else:
            return False

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i in range(0,self.BOARD_ROWS):
                for j in range(0,self.BOARD_COLS):
                    cell = self.board[i][j]
                    pix_x = cell.x * 30 + 350
                    pix_y = cell.y * 30 + 200
                    cell_rect = scaleRect(pix_x, pix_y, 28, 28)
                    if self.isIn(cell_rect,pos):
                        if event.button == 1:
                            cell.reveal()
                        if event.button == 3:
                            cell.flag()

    def on_key(self, key):
        pass

    def update(self):
        pass

    def isIn(self, object, position):
        test = object.collidepoint(position)
        return test

    def draw(self):
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                self.draw_cell(i,j)

    def draw_cell(self, x_pos, y_pos):
        cell = self.board[x_pos][y_pos]
        pix_x = cell.x*30+350
        pix_y = cell.y*30+200
        cell_rect = scaleRect(pix_x,pix_y,28,28)

        if cell.revealed:
            pygame.draw.rect(self.screen, Minesweeper.CELL_COLORS[0], cell_rect)
            if not (cell.is_mine or cell.flagged):
                drawText(self.screen,f"{cell.adjacent}",self.font,Minesweeper.CELL_COLORS[cell.adjacent], pix_x+10,pix_y+10)
            if cell.is_mine:
                pygame.draw.rect(self.screen, Minesweeper.CELL_COLORS[3], cell_rect)
                drawText(self.screen,'*',self.font,Minesweeper.CELL_COLORS[7],pix_x+15,pix_y+15)
        else:
            pygame.draw.rect(self.screen, Minesweeper.CELL_COLORS[8], cell_rect)
            if cell.flagged:
                drawText(self.screen, '#', self.font, Minesweeper.CELL_COLORS[3], pix_x + 15, pix_y + 15)


