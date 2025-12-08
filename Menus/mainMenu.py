import pygame
from pygame_widgets.button import Button
from Menus.gameSelect import initSelectMenu
import Menus.utils as utils


def drawMenuText(screen):
    text_font = pygame.font.SysFont("comicsans", 30)
    utils.draw_text(screen, "Main Menu", text_font, (0, 0, 0), 430, 100)

def initMainMenu(screen):
    def initGameSelect(screen):
        # Helper to switch menus
        utils.clear_objects()
        initSelectMenu(screen)

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
        onClick=lambda: initGameSelect(screen)
    )

    loginButton = Button(
        screen, 425, 410, 150, 60, text='Login', font= text_font,
        fontSize=50, margin=20,
        inactiveColour=(250, 150, 0),
        hoverColour=(200,150,0),
        pressedColour=(220, 150, 0),
        onClick=lambda: print('Click')
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
    textObjects = []
    menuObjects = buttons + textObjects

    # Object resizing (only done once - no future resizing)
    for object in menuObjects:
        object.setX(int(object.getX() * utils.scaleX))
        object.setY(int(object.getY() * utils.scaleY))
        object.setWidth(int(object.getWidth() * utils.scaleX))
        object.setHeight(int(object.getHeight() * utils.scaleY))
        utils.current_menu_objects.append(object)