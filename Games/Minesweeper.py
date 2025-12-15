from Games.BaseGame import BaseGame as Game, pygame
from Menus.utils import draw_text as drawText, setPreviousWinner as setWinner
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

            if self.is_mine:
                pass
            if not self.revealed and not self.flagged:
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
                    if 0 <= i < self.game.BOARD_ROWS and i != self.x:
                        if 0 <= j < self.game.BOARD_ROWS and j != self.y:
                            self.game.board[i][j].reveal()


        def flag(self):
            if self.flagged:
                self.flagged = False
            if not self.flagged:
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
        #self.board = [[Minesweeper.Cell(i,j,self) for i in range(self.BOARD_ROWS)] for j in range(self.BOARD_COLS)]
        #self.mines = [] # Where are the mines?
        #self.flags = [] # Which mines have been flagged by the player?
        #self.clicked = [] # what squares did the player click on?
        self.placeMines()
        self.revealAll()

    def revealAll(self):
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                self.board[i][j].reveal()

    def on_event(self, event):
        pass

    def on_key(self, keys):
        pass

    def update(self):
        pass

    def draw(self):
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                self.draw_cell(i,j)

    def draw_cell(self, x_pos, y_pos):
        cell = self.board[x_pos][y_pos]
        pix_x = cell.x*20+100
        pix_y = cell.y*20+300
        cell_rect = pygame.Rect(pix_x,pix_y, 18, 18)
        pygame.draw.rect(self.screen,color=Minesweeper.CELL_COLORS[0], rect=cell_rect)

        if cell.revealed:
            if not (cell.is_mine or cell.flagged):
                drawText(self.screen,f"{cell.adjacent}",self.font,Minesweeper.CELL_COLORS[cell.adjacent], pix_x+5,pix_y+5,)
            if cell.is_mine:
                drawText(self.screen,'*',self.font,(0,0,0),pix_x+5,pix_y+5)
            if cell.flagged:
                pass

