# Subclass used in Sudoku for storing various sudoku solving functions.
# Static class
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
        for row in board:
            for cell in row:
                if cell.playerNumber != -1:
                    cell.candidates = set()
                else:
                    cell.candidates = set(range(1, boardSize + 1))
                    for peer in cell.peers:
                        if peer.playerNumber != -1:
                            cell.candidates.discard(peer.playerNumber)

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
    # with that number. Also known as "naked singles" method.
    # Pseudocode taken from ChatGPT, code human-written.
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
    def buildUnits(board, boardSize, subgridSize):
        units = []

        # Rows
        for r in range(boardSize):
            units.append([board[r][c] for c in range(9)])

        # Columns
        for c in range(boardSize):
            units.append([board[r][c] for r in range(9)])

        # Boxes
        boxes = []
        for br in range(0, boardSize, subgridSize):
            for bc in range(0, boardSize, subgridSize):
                box = []
                for r in range(br, br + subgridSize):
                    for c in range(bc, bc + subgridSize):
                        box.append(board[r][c])
                units.append(box)
                boxes.append(box)

        return units, boxes

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

    # Look for naked pairs (https://www.learn-sudoku.com/naked-pairs.html)
    # Function written by chatgpt.
    @staticmethod
    def solvePairs(board, units):
        progress = False
        for unit in units:
            pairs = {}
            for cell in unit:
                if cell.playerNumber == -1 and len(cell.candidates) == 2:
                    key = frozenset(cell.candidates)
                    pairs.setdefault(key, []).append(cell)

            for pair, cells in pairs.items():
                if len(cells) == 2:
                    for cell in unit:
                        if cell not in cells and cell.playerNumber == -1:
                            if pair & cell.candidates:
                                cell.candidates -= pair
                                progress = True
        return progress

    # code written by ChatGPT
    @staticmethod
    def solvePointing(boxes, boardsize):
        progress = False
        for box in boxes:
            for digit in range(1, boardsize + 1):
                cells = [c for c in box if c.playerNumber == -1 and digit in c.candidates]
                if not cells:
                    continue

                rows = {c.row for c in cells}
                cols = {c.col for c in cells}

                if len(rows) == 1:
                    r = rows.pop()
                    for c in range(boardsize):
                        cell = box[0].board[r][c]
                        if cell not in cells and digit in cell.candidates:
                            cell.candidates.remove(digit)
                            progress = True

                if len(cols) == 1:
                    c = cols.pop()
                    for r in range(boardsize):
                        cell = box[0].board[r][c]
                        if cell not in cells and digit in cell.candidates:
                            cell.candidates.remove(digit)
                            progress = True
        return progress