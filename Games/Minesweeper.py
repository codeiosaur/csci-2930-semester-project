from Games.BaseGame import BaseGame as Game, pygame
from Menus.utils import draw_text as drawText, setPreviousWinner as setWinner
import random

class Minesweeper(Game):
    class Cell:
        def __init__(self):
            self.is_mine = False
            self.adjacent = 0
            self.revealed = False
            self.flagged = False

    def __init__(self, screen):
        super().__init__(screen)
        # Minesweeper constants here - mines depending on difficulty
        self.BOARD_ROWS = self.BOARD_COLS = 10
        self.TOTAL_MINES = 10
        self.run()

        # Place the mines in random locations
        def placeMines(self):
            pass

        def setup(self):
            self.board = [[Minesweeper.Cell() for _ in range(self.BOARD_COLS)] for _ in range(self.BOARD_ROWS)]
            self.mines = [] # Where are the mines?
            self.flags = [] # Which mines have been flagged by the player?
            self.clicked = [] # what squares did the player click on?

