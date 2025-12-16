from Games.BaseGame import BaseGame as Game, pygame
from Games.SudokuSolver import SudokuSolver
from Menus.utils import draw_text as drawText, setPreviousWinner as setWinner
import random
from copy import deepcopy

# Main Author: Alex

class Sudoku(Game):
    class Cell:
        def __init__(self, row, col):
            self.playerNumber = -1 # what number did the player write?
            self.correctNumber = -1
            self.correct = None
            self.clickable = True # can the player change it?
            self.row = row
            self.col = col
            # Used in ChatGPT-made functions
            self.candidates = set()
            self.peers = set()

        def __repr__(self):
            return str(f"{self.playerNumber}") if self.playerNumber != -1 else " "

    def __init__(self, screen):
        super().__init__(self)
        # Sudoku constants
        self.SUBGRID_SIZE = 3 # same # of rows and cols
        self.BOARD_SIZE = self.SUBGRID_SIZE ** 2 # same number of subgrids in rows and cols
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.board = []
        self.run()

    # Checks whether a given sudoku is valid.
    # Used after switching numbers around.
    # Adapted from https://www.geeksforgeeks.org/dsa/check-if-given-sudoku-solution-is-valid-or-not/.
    def checkValidity(self):
        # Track of numbers in rows, columns, and sub-matrix
        rows = [[0] * (self.BOARD_SIZE + 1) for _ in range(self.BOARD_SIZE)]
        cols = [[0] * (self.BOARD_SIZE + 1) for _ in range(self.BOARD_SIZE)]
        regs = [[0] * (self.BOARD_SIZE + 1) for _ in range(self.BOARD_SIZE)] # regions

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                # Skip empty cells
                if self.board[i][j] == 0:
                    continue
                # Current value
                val = self.board[i][j].correctNumber
                # Check for duplicates in row
                if rows[i][val] == 1:
                    return False
                # Mark as seen
                rows[i][val] = 1
                # Check for duplicates in column
                if cols[j][val] == 1:
                    return False
                # Mark as seen
                cols[j][val] = 1
                # Check for duplicates in sub-grid
                idx = (i // self.SUBGRID_SIZE) * self.SUBGRID_SIZE + j // self.SUBGRID_SIZE
                if regs[idx][val] == 1:
                    return False
                # Mark as seen
                regs[idx][val] = 1
        return True

    def setNumPattern(self, row, col):
        basesize = self.SUBGRID_SIZE
        return (basesize * (row % basesize) + row // basesize + col) % self.BOARD_SIZE

    def shuffleRow(self, arr):
        return random.sample(arr, len(arr))

    def swapCells(self, row1, col1, row2, col2):
        tempCell = deepcopy(self.board[row1][col1])
        self.board[row1][col1] = self.board[row2][col2]
        self.board[row2][col2] = tempCell

    def generateSudoku(self):
        # Unless stated otherwise, this function, as well as shuffleRow and setNumPattern,
        # are adapted from ChatGPT and this stack overflow response:
        # https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python
        # base pattern
        self.board = [[Sudoku.Cell(r, c) for r in range(self.BOARD_SIZE)] for c in range(self.BOARD_SIZE)]
        rows = [g * self.SUBGRID_SIZE + r for g in self.shuffleRow(range(self.SUBGRID_SIZE))
                for r in self.shuffleRow(range(self.SUBGRID_SIZE))]
        cols = [g * self.SUBGRID_SIZE + c for g in self.shuffleRow(range(self.SUBGRID_SIZE))
                for c in self.shuffleRow(range(self.SUBGRID_SIZE))]
        # shuffle numbers - also adapted from stackoverflow
        nums = self.shuffleRow(range(1, self.BOARD_SIZE + 1))
        nums = [ [nums[self.setNumPattern(r,c)] for c in cols ] for r in rows ]

        # copy numbers to cell structure
        for r in rows:
            for c in cols:
                self.board[r][c].correctNumber = nums[r][c]
                self.board[r][c].playerNumber = self.board[r][c].correctNumber
                self.board[r][c].clickable = False

        SudokuSolver.setPeers(self.board, self.SUBGRID_SIZE, self.BOARD_SIZE)
        self.createPuzzle()

    def createPuzzle(self):
        cellPosQueue = [(r, c) for r in range(self.SUBGRID_SIZE) for c in range(self.BOARD_SIZE)]
        random.shuffle(cellPosQueue)

        # used for hidden singles and pointing pairs functions in solver
        units = SudokuSolver.buildUnits(self.board, self.BOARD_SIZE, self.SUBGRID_SIZE)
        hiddenUnits = units[0]; pointingBoxes = units[1]

        # Main removal
        removedCells = 0; attempts = 60
        while len(cellPosQueue) > 1 and removedCells < attempts:
            currPos1 = cellPosQueue.pop()  # current cell position
            currPos2 = [self.BOARD_SIZE - currPos1[0] - 1, self.BOARD_SIZE - currPos1[1] - 1]
            currCell1 = self.board[currPos1[0]][currPos1[1]]
            currCell2 = self.board[currPos2[0]][currPos2[1]]

            # Attempt removal of cell
            # Function was human written up until this point but is now ChatGPT-debugged.
            currCell1.playerNumber = -1; currCell2.playerNumber = -1
            for row in self.board:
                for cell in row:
                    SudokuSolver.createCandidates(cell, self.board, self.BOARD_SIZE)
            progress = True
            while progress:
                progress = False
                if SudokuSolver.solveLRC(self.board, self.BOARD_SIZE): progress = True
                if SudokuSolver.solveHidden(self.board, self.BOARD_SIZE, hiddenUnits): progress = True
                if SudokuSolver.solvePairs(self.board, hiddenUnits): progress = True
                if SudokuSolver.solvePointing(pointingBoxes, self.BOARD_SIZE): progress = True

            currCell1.clickable = True  # make it so player can change it
            currCell2.clickable = True
            removedCells += 2

        # Middle grid removal
        midRemovals = random.randint(6, 18)
        cellPosQueue = [(r, c) for r in range(self.SUBGRID_SIZE, self.SUBGRID_SIZE * 2)
                         for c in range(self.BOARD_SIZE)]
        random.shuffle(cellPosQueue)
        for i in range(midRemovals):
            currPos = cellPosQueue.pop()  # current cell position
            currCell = self.board[currPos[0]][currPos[1]]
            currCell.playerNumber = -1
            currCell.clickable = True

        # Update candidates after middle grid removal
        for row in self.board:
            for cell in row:
                SudokuSolver.createCandidates(cell, self.board, self.BOARD_SIZE)

    def setup(self):
        self.generateSudoku()

    def on_event(self, event):
        pass

    def on_key(self, keys):
        pass

    def update(self):
        pass

    def draw(self):
        pass