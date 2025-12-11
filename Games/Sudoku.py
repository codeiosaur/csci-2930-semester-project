from Games.BaseGame import BaseGame as Game, pygame
from Menus.utils import draw_text as drawText, setPreviousWinner as setWinner
import random



class Sudoku(Game):
    class Cell:
        def __init__(self):
            self.playerNumber = -1 # what number did the player write
            self.correctNumber = -1
            self.correct = None
            self.clickable = True # can the player change it?

        def __repr__(self):
            return str(self.correctNumber)

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
        nums = self.shuffleRow(range(1, self.BOARD_SIZE + 1))

        # initial base pattern method
        for r in rows:
            for c in cols:
                board[r][c].correctNumber = nums[self.setNumPattern(r, c)]
                board[r][c].playerNumber = board[r][c].correctNumber
                board[r][c].clickable = False
        for row in board:
            print(row)

        # Randomly switch around some of the numbers
        row1, row2 = random.randint(1, self.BOARD_SIZE)
        col1, col2 = random.randint(1, self.BOARD_SIZE)


        return board

    def setup(self):
        board = self.generateSudoku()

    def on_event(self, event):
        pass

    def on_key(self, keys):
        pass

    def update(self):
        pass

    def draw(self):
        pass
