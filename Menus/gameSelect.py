import pygame
from pygame_widgets.button import Button
from Menus import utils as utils
from Games import Pong

def drawMenuText(screen):
    text_font = pygame.font.SysFont("comicsans", 30)
    utils.draw_text(screen, "Shall we play a game?", text_font, (0, 0, 0), 500, 100)

def startPong(screen):
    Pong.Pong(screen) # If this stops executing, the game must have ended.
    utils.setPreviousGame("Pong")
    utils.switchMenus("gameOver")

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
        onClick=lambda: startPong(screen)
    )

    buttons = [pongButton]

    for button in buttons:
        button.setX(int(button.getX() * screenInfo["scaleX"]))
        button.setY(int(button.getY() * screenInfo["scaleY"]))
        button.setWidth(int(button.getWidth() * screenInfo["scaleX"]))
        button.setHeight(int(button.getHeight() * screenInfo["scaleY"]))
        utils.register_widget(button)