from Games.BaseGame import BaseGame as Game, pygame
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

        def __repr__(self):
            #return str(f"Cell at {self.row},{self.col}: {self.correctNumber}")
            return str(f"{self.playerNumber}")

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
                idx = (i // 3) * 3 + j // 3
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

        self.createPuzzle()

    def createPuzzle(self):
        cellPosQueue = [(r, c) for r in range(self.SUBGRID_SIZE) for c in range(self.BOARD_SIZE)]
        random.shuffle(cellPosQueue)
        removedCells = 0
        while removedCells < 9:
            currPos = cellPosQueue.pop(0)  # current cell position
            currCell = self.board[currPos[0]][currPos[1]]
            currCell.playerNumber = -1  # hide it
            print(f"removing cell {currPos}")
            removalLegal = SudokuSolver.lastFreeCell(currCell, self.board,
                                                     self.SUBGRID_SIZE, self.BOARD_SIZE)
            if removalLegal:
                print("success")
                currCell.clickable = True  # make it so player can change it
                removedCells += 1
            else:
                print("failure")
                # if removal leads to no or more than 1 solution
                cellPosQueue.append(currPos)
                currCell.playerNumber = currCell.correctNumber
                removedCells += 1



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


# Static class used for storing various sudoku solving functions
class SudokuSolver:
    @staticmethod
    def findEmptyCells(board, subgridSize, boardSize):
        emptyCells = []
        for row in range(boardSize):
            for col in range(boardSize):
                if board[row][col].playerNumber == -1:
                    emptyCells.append((row, col))
        return emptyCells



    # Takes a given cell position. Based on the "last free cell" method
    # (https://sudoku.com/sudoku-rules/last-free-cell/),
    # Looks for the numbers that can be at cellPos based on the other #s in the row/col/box.
    # Returns True if exactly 1 solution can be reached after removing this cell.
    @staticmethod
    def lastFreeCell(cell, board, subgridSize, boardSize):
        counter = 0
        for row in board:
            print(f"Row {counter}: {row}")
            counter += 1
        # Are there 8 other visible cells in the same row?
        # If so, only 1 number can fit in cellPos - the one not among the other 8.
        # (A cell where playerNumber is -1 is blank and therefore not visible.)
        numsFound = [] # board is always square so range should always be the same.
        for row in range(boardSize):
            if board[cell.col][row].playerNumber != -1:
                numsFound.append(board[cell.col][row].playerNumber)
        print(f"Nums found (row): {numsFound}")
        if len(numsFound) == boardSize - 1:
            # Only one possible number can be put into the current cell - one solution
            return True
        # Are there 8 other viewable cells in the same column?
        numsFound.clear()
        for col in range(boardSize):
            if board[cell.row][col].playerNumber != -1:
                numsFound.append(board[cell.row][col].playerNumber)
        print(f"Nums found (col): {numsFound}")
        if len(numsFound) == boardSize - 1:
            return True
        # Are there 8 other viewable cells in the same box/subgrid?
        numsFound.clear()
        for row in range(subGrid[0] * subgridSize, (subGrid[0] + 1) * subgridSize):
            for col in range(subGrid[1] * subgridSize, (subGrid[1] + 1) * subgridSize):
                if board[row][cell.col] != -1:
                    numsFound.append(board[row][col].playerNumber)
        print(f"Nums found (box): {numsFound}")
        if len(numsFound) == boardSize - 1:
            return True
        else:
            # CAN still be solvable, just not with this method.
            return False

    @staticmethod
    def lastFreeCell(cell, board, subgridSize, boardSize):
        # Based on the "last free cell" method
        # (https://sudoku.com/sudoku-rules/last-free-cell/),
        # Looks for the numbers that can be filled in based on the other #s in the row/col/box.
        # Returns True if exactly 1 solution can be reached without guessing.
        counter = 0
        # for row in board:
        #     print(f"Row {counter}: {row}")
        #     counter += 1
        # Figure out in which subgrid the cell is in. ([0, 0] is the top-left subgrid.)

        # Look for all empty cells on the board.
        emptyCells = SudokuSolver.findEmptyCells(board, subgridSize, boardSize)

        # Can the empty cells be solved with the "last free cell" method?
        for cell in emptyCells:
            # Figure out in which subgrid the cell is in. ([0, 0] is the top-left subgrid.)
            subGrid = [cell.row // subgridSize, cell.col // subgridSize]

            # board is always square so range should always be the same.
            numsNotFound = [range(1, boardSize + 1)]

            # Are there 8 other visible cells in the same row?
            # If so, only 1 number can fit in cellPos - the one not among the other 8.
            # (A cell where playerNumber is -1 is blank and therefore not visible.)
            for row in range(boardSize):
                if board[cell.col][row].playerNumber != -1:
                    numsNotFound.remove(board[cell.col][row].playerNumber)
            print(f"Nums not found (row): {numsNotFound}")
            if len(numsNotFound) == 1:
                # Only 1 number not found - cell must be this number.
                emptyCells.remove(cell)

            # Are there 8 other viewable cells in the same column?
            numsNotFound.clear()
            for col in range(boardSize):
                if board[cell.row][col].playerNumber != -1:
                    numsNotFound.append(board[cell.row][col].playerNumber)
            print(f"Nums not found (col): {numsNotFound}")
            if len(numsNotFound) == 1:
                emptyCells.remove(cell)

            # Are there 8 other viewable cells in the same box/subgrid?
            numsNotFound.clear()
            for row in range(subGrid[0] * subgridSize, (subGrid[0] + 1) * subgridSize):
                for col in range(subGrid[1] * subgridSize, (subGrid[1] + 1) * subgridSize):
                    if board[row][cell.col].playerNumber != -1:
                        numsNotFound.append(board[row][col].playerNumber)
            print(f"Nums not found (box): {numsNotFound}")
            if len(numsNotFound) == boardSize - 1:
                emptyCells.remove(cell)








