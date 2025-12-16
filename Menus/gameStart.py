import pygame
from pygame_widgets.button import Button
from Menus import utils as utils


current_game = None

def drawMenuText(screen):
    text_font = pygame.font.SysFont("comicsans", 30)
    utils.draw_text(screen, current_game, text_font, (0, 0, 0), 500, 100)

def startPong(screen):
    from Games import Pong
    Pong.Pong(screen) # If this stops executing, the game must have ended.
    utils.setPreviousGame("Pong")
    utils.switchMenus("gameOver")

def startMinesweeper(screen):
    from Games import Minesweeper
    Minesweeper.Minesweeper(screen)
    #utils.setPreviousGame("Minesweeper")
    #utils.switchMenus("gameOver")

def startMastermind(screen):
    from Games import Mastermind
    Mastermind.Mastermind(screen)

def startSudoku(screen):
    from Games import Sudoku
    Sudoku.Sudoku(screen)

def startGame(screen):
    if current_game == "Pong":
        startPong(screen)
    if current_game == "Minesweeper":
        startMinesweeper(screen)
    if current_game == "Sudoku":
        startSudoku(screen)


def initGameStart(screen):
    screenInfo = utils.getScreenDims()
    utils.clear_objects()
    screen.fill((255, 255, 255))
    drawMenuText(screen)

    utils.switchMenus("gameStart")
    text_font = pygame.font.SysFont("comicsans", 30)

    # Buttons init
    startButton = Button(
        screen, 375, 460, 250, 100, text='Start Game', font=text_font,
        fontSize=50, margin=20,
        inactiveColour=(1, 150, 150),
        hoverColour=(100, 100, 100),
        pressedColour=(180, 180, 180),
        onClick=lambda: startGame(screen)
    )
    backButton = Button(
        screen, 405, 580, 200, 60, text='Back to Game Select', font=text_font,
        fontSize=50, margin=20,
        inactiveColour=(150, 150, 150),
        hoverColour=(100, 100, 100),
        pressedColour=(180, 180, 180),
        onClick=lambda: utils.switchMenus("gameSelect")
    )

    buttons = [startButton, backButton]

    for button in buttons:
        button.setX(int(button.getX() * screenInfo["scaleX"]))
        button.setY(int(button.getY() * screenInfo["scaleY"]))
        button.setWidth(int(button.getWidth() * screenInfo["scaleX"]))
        button.setHeight(int(button.getHeight() * screenInfo["scaleY"]))
        utils.register_widget(button)