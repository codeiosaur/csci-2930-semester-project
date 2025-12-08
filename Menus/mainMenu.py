import pygame
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from Menus.gameSelect import initSelectMenu
import Menus.utils as utils
from Menus.utils import current_menu_objects


def initMainMenu(screen):
    def initGameSelect(screen):
        #Helper to switch menus
        utils.clear_objects()
        initSelectMenu(screen)

    # Other initializations (non-button)
    text_font = pygame.font.SysFont("comicsans", 30)
    bg_color = (255, 255, 255)
    pygame.display.set_caption("Main Window")

    # Text init
    title = TextBox(
        screen, int(375 * utils.scaleX), int(100 * utils.scaleY),
        int(400 * utils.scaleX), int(80 * utils.scaleY),
        fontSize=int(50 * utils.scaleY),
        colour=(255, 255, 255),
        textColour=(0, 0, 0),
        borderThickness = 0
    )
    title.setText("Main Menu")

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
    textObjects: list[TextBox] = [title]
    menuObjects = buttons + textObjects

    # Button resizing (only done once - no future resizing)
    # for button in buttons:
    #     button.setX(int(button.getX() * utils.scaleX))
    #     button.setY(int(button.getY() * utils.scaleY))
    #     button.setWidth(int(button.getWidth() * utils.scaleX))
    #     button.setHeight(int(button.getHeight() * utils.scaleY))
    for object in menuObjects:
        object.setX(int(object.getX() * utils.scaleX))
        object.setY(int(object.getY() * utils.scaleY))
        object.setWidth(int(object.getWidth() * utils.scaleX))
        object.setHeight(int(object.getHeight() * utils.scaleY))
        current_menu_objects.append(object)