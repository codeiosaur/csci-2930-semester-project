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

        # used for hidden singles function in solver
        hiddenUnits = SudokuSolver.buildUnits(self.board, self.BOARD_SIZE, self.SUBGRID_SIZE)

        for row in self.board:
            print(row)
        print("-----")

        removedCells = 0; targetCells = 60
        while len(cellPosQueue) > 1 and removedCells < targetCells:
            currPos1 = cellPosQueue.pop()  # current cell position
            currPos2 = [self.BOARD_SIZE - currPos1[0] - 1, self.BOARD_SIZE - currPos1[1] - 1]
            currCell1 = self.board[currPos1[0]][currPos1[1]]
            currCell2 = self.board[currPos2[0]][currPos2[1]]

            backupBoard = deepcopy(self.board)
            # Attempt removal of cell
            # Function was human written up until this point but is now ChatGPT-debugged.
            currCell1.playerNumber = -1; currCell2.playerNumber = -1
            for row in self.board:
                for cell in row:
                    SudokuSolver.createCandidates(cell, self.board, self.BOARD_SIZE)
            progress = True
            while progress:
                progress = False
                if (SudokuSolver.solveLRC(self.board, self.BOARD_SIZE)):
                    progress = True
                if (SudokuSolver.solveHidden(self.board, self.BOARD_SIZE, hiddenUnits)):
                    progress = True

            print("success")
            currCell1.clickable = True  # make it so player can change it
            currCell2.clickable = True
            removedCells += 2

        print("finished")
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
# All functions/code written and debugged by Alex unless otherwise stated.
class SudokuSolver:
    @staticmethod
    def findEmptyCells(board, boardSize):
        emptyCells = []
        for row in range(boardSize):
            for col in range(boardSize):
                if board[row][col].playerNumber == -1:
                    emptyCells.append([row, col])
        return emptyCells

    # Code adapted from ChatGPT for this function, setPeers, and setValue.
    # createCandidates was generated as Python; the latter two are from pseudocode.
    @staticmethod
    def createCandidates(cell, board, boardSize):
        # Assumes empty cell.
        # Step 1: Update the cell itself
        cell.candidates = set(range(1, boardSize + 1))
        for peer in cell.peers:
            if peer.playerNumber != -1:
                cell.candidates.discard(peer.playerNumber)

        # Step 2: Update all peers
        for peer in cell.peers:
            if peer.playerNumber == -1:
                # Remove all filled numbers from peer's candidates
                peer.candidates = set(range(1, boardSize + 1))
                for p2 in peer.peers:
                    if p2.playerNumber != -1:
                        peer.candidates.discard(p2.playerNumber)

    @staticmethod
    def setPeers(board, subgridSize, boardSize):
        for r in range(0, boardSize):
            for c in range(0, boardSize):
                cell = board[r][c]
                cell.peers = set()

                # Add row peers
                for i in range(0, boardSize):
                    if i != c:
                        cell.peers.add(board[r][i])

                # Add column peers
                for i in range(0, boardSize):
                    if i != r:
                        cell.peers.add(board[i][c])

                # Figure out in which subgrid the cell is in. ([0, 0] is the top-left subgrid.)
                subGrid = [cell.row // subgridSize, cell.col // subgridSize]
                # Then add box/subgrid peers.
                for dr in range(subgridSize):
                    for dc in range(subgridSize):
                        r2 = subGrid[0] + dr
                        c2 = subGrid[1] + dc
                        if r2 == r and c2 == c:
                            continue
                        cell.peers.add(board[r2][c2])

    @staticmethod
    def setValue(cell, value):
        cell.playerNumber = value
        cell.candidates = set()
        for peer in cell.peers:
            if peer.playerNumber == -1:
                peer.candidates.discard(value)

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

    # Pseudocode taken from ChatGPT, code human-written
    @staticmethod
    def solveLRC(board, boardSize):
        progress = True
        while progress:
            progress = False
            for row in range(boardSize):
                for col in range(boardSize):
                    cell = board[row][col]
                    if cell.playerNumber == -1 and len(cell.candidates) == 1:
                        value = next(iter(cell.candidates))
                        SudokuSolver.setValue(cell, value)
                        progress = True
        return progress

    # Stores various units, rows, and columns. Used in the hidden singles function
    # (because it checks if a number can only go one place somewhere).
    # Written by ChatGPT.
    @staticmethod
    def buildUnits(board, boardsize, subgridsize):
        units = []

        # Rows
        for r in range(boardsize):
            units.append([board[r][c] for c in range(9)])

        # Columns
        for c in range(boardsize):
            units.append([board[r][c] for r in range(9)])

        # Boxes
        for br in range(0, boardsize, subgridsize):
            for bc in range(0, boardsize, subgridsize):
                box = []
                for r in range(br, br + subgridsize):
                    for c in range(bc, bc + subgridsize):
                        box.append(board[r][c])
                units.append(box)

        return units

    # Solve with hidden singles method.
    # Code chatgpt-written, then adapted for custom boards.
    @staticmethod
    def solveHidden(board, boardsize, units):
        progress = True

        while progress:
            progress = False

            # Naked singles
            for row in board:
                for cell in row:
                    if cell.playerNumber == -1 and len(cell.candidates) == 1:
                        value = next(iter(cell.candidates))
                        SudokuSolver.setValue(cell, value)
                        progress = True

            # Hidden singles
            for unit in units:
                positions = {d: [] for d in range(1, boardsize + 1)}

                for cell in unit:
                    if cell.playerNumber == -1:
                        for d in cell.candidates:
                            positions[d].append(cell)

                for d in range(1, boardsize + 1):
                    if len(positions[d]) == 1:
                        cell = positions[d][0]
                        SudokuSolver.setValue(cell, d)
                        progress = True
        return progress

