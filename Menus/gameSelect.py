import pygame
from pygame_widgets.button import Button
from Menus import utils, gameStart
from Menus.gameStart import initGameStart


# Main Author: Alex

def drawMenuText(screen):
    text_font = pygame.font.SysFont("comicsans", 30)
    utils.draw_text(screen, "Shall we play a game?", text_font, (0, 0, 0), 500, 100)
"""
def startPong(screen):
    from Games import Pong
    Pong.Pong(screen) # If this stops executing, the game must have ended.
    utils.setPreviousGame("Pong")
    utils.switchMenus("gameOver")

def startMinesweeper(screen):
    from Games import Minesweeper
    Minesweeper.Minesweeper(screen)
    utils.setPreviousGame("Minesweeper")
    utils.switchMenus("gameOver")

def startSudoku(screen):
    from Games import Sudoku
    Sudoku.Sudoku(screen)
"""

def startGame(game):
    gameStart.current_game = game
    utils.switchMenus("gameStart")
    if game == "Minesweeper":
        gameStart.current_game_point = False
    else:
        gameStart.current_game_point = True

def initSelectMenu(screen):
    screenInfo = utils.getScreenDims()
    utils.clear_objects()
    screen.fill((255, 255, 255))
    drawMenuText(screen)

    utils.switchMenus("gameSelect")
    text_font = pygame.font.SysFont("comicsans", 30)

    # Buttons init
    pongButton = Button(
        screen, 425, 480, 150, 60, text='Pong', font=text_font,
        fontSize=50, margin=20,
        inactiveColour=(150, 150, 150),
        hoverColour=(100, 100, 100),
        pressedColour=(180, 180, 180),
        onClick=lambda: startGame("Pong")
    )

    mineButton = Button(
        screen, 625, 480, 150, 60, text='Minesweeper', font=text_font,
        textColor = (0, 0, 0), fontSize=50, margin=20,
        inactiveColour=(250, 0, 0),
        hoverColour=(200, 0, 0),
        pressedColour=(220, 0, 0),
        onClick=lambda: startGame("Minesweeper")
    )

    sudokuButton = Button(
        screen, 525, 280, 150, 60, text='Sudoku', font=text_font,
        textColor=(0, 0, 0), fontSize=50, margin=20,
        inactiveColour=(0, 200, 0),
        hoverColour=(0, 150, 0),
        pressedColour=(0, 220, 0),
        onClick=lambda: startGame("Sudoku")
    )

    """mastermindButton = Button(
        screen, 205, 380, 150, 60, text='Mastermind', font=text_font,
        fontSize=50, margin=20,
        inactiveColour=(150, 0, 150),
        hoverColour=(100, 100, 100),
        pressedColour=(180, 180, 180),
        onClick=lambda: startGame("Mastermind")
    )"""

    buttons = [pongButton, mineButton, sudokuButton]

    for button in buttons:
        button.setX(int(button.getX() * screenInfo["scaleX"]))
        button.setY(int(button.getY() * screenInfo["scaleY"]))
        button.setWidth(int(button.getWidth() * screenInfo["scaleX"]))
        button.setHeight(int(button.getHeight() * screenInfo["scaleY"]))
        utils.register_widget(button)