from Games.BaseGame import BaseGame as Game, pygame
from Menus.utils import draw_text as drawText, setPreviousWinner as setWinner
import random
from copy import deepcopy

# Main Author: Alex

class Sudoku(Game):
    class Cell:
        def __init__(self, row, col, boardsize):
            self.playerNumber = -1 # what number did the player write?
            self.correctNumber = -1
            self.correct = None
            self.clickable = True # can the player change it?
            self.row = row
            self.col = col
            self.candidates = set(range(1, boardsize + 1))

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

        for row in self.board:
            print(row)
        print("-----")
        removedCells = 0
        while removedCells < 9:
            currPos = cellPosQueue.pop(0)  # current cell position
            currCell = self.board[currPos[0]][currPos[1]]
            currCell.playerNumber = -1  # hide it
            removalLegal = (SudokuSolver.solvePuzzle(deepcopy(self.board), self.SUBGRID_SIZE, self.BOARD_SIZE))
            if removalLegal:
                currCell.clickable = True  # make it so player can change it
                removedCells += 1
            else:
                # if removal leads to no or more than 1 solution, put the cell back
                cellPosQueue.append(currPos)
                currCell.playerNumber = currCell.correctNumber

        for row in self.board:
            print(row)



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
    def findEmptyCells(board, boardSize):
        emptyCells = []
        for row in range(boardSize):
            for col in range(boardSize):
                if board[row][col].playerNumber == -1:
                    emptyCells.append([row, col])
        return emptyCells


    # Tries to solve the puzzle.
    @staticmethod
    def solvePuzzle(board, subgridSize, boardSize):
        emptyCells = SudokuSolver.findEmptyCells(board, subgridSize)
        progress = False
        # Last remaining cell algorithm
        for cell in emptyCells:
            # Figure out in which subgrid the cell is in. ([0, 0] is the top-left subgrid.)
            subGrid = [cell[0] // subgridSize, cell[1] // subgridSize]

            # board is always square so range should always be the same.
            numsUsed = set()

            # First check for numbers eliminated due to being in the same row.
            for col in range(boardSize):
                if (board[cell[0]][col].playerNumber != -1):
                    numsUsed.add(board[cell[0]][col].playerNumber)

            # Check for numbers in the same column.
            for row in range(boardSize):
                if board[row][cell[1]].playerNumber != -1:
                    numsUsed.add(board[row][cell[1]].playerNumber)

            # Check for numbers in the same box.
            for row in range(subGrid[0] * subgridSize, (subGrid[0] + 1) * subgridSize):
                for col in range(subGrid[1] * subgridSize, (subGrid[1] + 1) * subgridSize):
                    if board[row][col].playerNumber != -1:
                        numsUsed.add(board[row][col].playerNumber)

            if (len(numsUsed) == 1
                    and board[cell[0]][cell[1]].correctNumber not in numsUsed):
                emptyCells.remove(cell)
                board[cell[0]][cell[1]].playerNumber = board[cell[0]][cell[1]].correctNumber




    # Based on the "last remaining cell" method (https://sudoku.com/sudoku-rules/last-remaining-cell/).
    # When trying to put a given number in a box, if more than 1 space in a box is blank,
    # but all but 1 space are blocked by numbers in different rows/cols, the 1 space must be filled
    # with that number. Returns True if all empty cells can be filled in with this method.
    # Also known as "naked singles" method.
    @staticmethod
    def lastRemCell(board, subgridSize, boardSize):
        # Look for all empty cells on the board.
        emptyCells = SudokuSolver.findEmptyCells(board, subgridSize)
        # Can the empty cells be solved with the "last remaining cell" method?
        cellsRemoved = 1
        while cellsRemoved != 0:
            cellsRemoved = 0
            for cell in emptyCells:
                # Figure out in which subgrid the cell is in. ([0, 0] is the top-left subgrid.)
                subGrid = [cell[0] // subgridSize, cell[1] // subgridSize]

                # board is always square so range should always be the same.
                numsUsed = set()
                # First check for numbers eliminated due to being in the same row.
                for col in range(boardSize):
                    if (board[cell[0]][col].playerNumber != -1):
                        numsUsed.add(board[cell[0]][col].playerNumber)
                if (len(numsUsed) == boardSize - 1
                    and board[cell[0]][cell[1]].correctNumber not in numsUsed):
                    emptyCells.remove(cell); cellsRemoved += 1
                    continue

                # Check for numbers in the same column.
                for row in range(boardSize):
                    if board[row][cell[1]].playerNumber != -1:
                        numsUsed.add(board[row][cell[1]].playerNumber)
                if (len(numsUsed) == boardSize - 1
                    and board[cell[0]][cell[1]].correctNumber not in numsUsed):
                    emptyCells.remove(cell); cellsRemoved += 1
                    continue

                # Check for numbers in the same box.
                for row in range(subGrid[0] * subgridSize, (subGrid[0] + 1) * subgridSize):
                    for col in range(subGrid[1] * subgridSize, (subGrid[1] + 1) * subgridSize):
                        if board[row][col].playerNumber != -1:
                            numsUsed.add(board[row][col].playerNumber)
                if (len(numsUsed) == 1
                        and board[cell[0]][cell[1]].correctNumber not in numsUsed):
                    emptyCells.remove(cell); cellsRemoved += 1

    @staticmethod
    def solveLRC(board, subgridSize, boardSize):
        progress = True
        while progress:
            pass






