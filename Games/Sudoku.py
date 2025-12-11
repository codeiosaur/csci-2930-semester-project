from Games.BaseGame import BaseGame as Game, pygame
from Menus.utils import draw_text as drawText, setPreviousWinner as setWinner
import random

class Sudoku(Game):
    class Cell:
        def __init__(self):
            self.playerNumber = -1 # what number did the player write
            self.correctNumber = -1
            self.correct = None

    def __init__(self, screen):
        super().__init__(self)
        # Sudoku constants
        self.SUBGRID_SIZE = 3 # same # of rows and cols
        self.BOARD_SIZE = self.SUBGRID_SIZE ** 2 # same number of subgrids in rows and cols
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.run()

    def setNumPattern(self, row, col):
        basesize = self.SUBGRID_SIZE
        return (basesize * (row % basesize) + row // basesize + col) % self.BOARD_SIZE

    def shuffleRow(self, arr):
        return random.sample(arr, len(arr))

    def generateSudoku(self):
        board = [[Sudoku.Cell() for r in range(self.BOARD_SIZE)] for c in range(self.BOARD_SIZE)]
        rows = [g * self.SUBGRID_SIZE + r for g in self.shuffleRow(range(self.SUBGRID_SIZE))
                for r in self.shuffleRow(range(self.SUBGRID_SIZE))]
        cols = [g * self.SUBGRID_SIZE + c for g in self.shuffleRow(range(self.SUBGRID_SIZE))
                for c in self.shuffleRow(range(self.SUBGRID_SIZE))]
        nums = self.shuffleRow(range(1, self.SUBGRID_SIZE + 1))

        # build the board
        board = [[nums[self.setNumPattern(r, c)] for c in cols] for r in rows]
        for row in board:
            print(row)
        return board

    def setup(self):
        pass

    def on_event(self, event):
        pass

    def on_key(self, keys):
        pass

    def update(self):
        pass

    def draw(self):
        pass
