import pygame
from pygame_widgets.button import Button
import Menus.utils as utils

def drawMenuText(screen):
    text_font = pygame.font.SysFont("comicsans", 30)
    utils.draw_text(screen, "Main Menu", text_font, (0, 0, 0), 500, 100)

def initMainMenu(screen):
    screenInfo = utils.getScreenDims()
    utils.clear_objects()
    drawMenuText(screen)

    utils.current_menu = "main"

    # Other initializations (non-button)
    text_font = pygame.font.SysFont("comicsans", 30)
    pygame.display.set_caption("Main Window")

    # Buttons init
    startButton = Button(
        screen, 375, 250, 250, 150, text='Start', font= text_font,
        fontSize=50, margin=20,
        inactiveColour=(0, 200, 0),
        hoverColour=(0,150,0),
        pressedColour=(0, 220, 0),
        onClick=lambda: utils.switchMenus("gameSelect")
    )

    loginButton = Button(
        screen, 425, 410, 150, 60, text='Login', font= text_font,
        fontSize=50, margin=20,
        inactiveColour=(250, 150, 0),
        hoverColour=(200,150,0),
        pressedColour=(220, 150, 0),
        onClick=lambda: utils.switchMenus("login")
    )

    settingsButton = Button(
        screen, 425, 480, 150, 60, text='Settings', font= text_font,
        fontSize=50, margin=20,
        inactiveColour=(150, 150, 150),
        hoverColour=(100,100,100),
        pressedColour=(180, 180, 180),
        onClick=lambda: print('Click')
    )
    buttons = [startButton, loginButton, settingsButton]
    menuObjects = buttons

    # Object resizing (only done once - no future resizing)
    for object in menuObjects:
        object.setX(int(object.getX() * screenInfo["scaleX"]))
        object.setY(int(object.getY() * screenInfo["scaleY"]))
        object.setWidth(int(object.getWidth() * screenInfo["scaleX"]))
        object.setHeight(int(object.getHeight() * screenInfo["scaleY"]))
        utils.register_widget(object)