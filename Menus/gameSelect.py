import pygame
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import Menus.utils as utils
from Games import Pong

def drawMenuText(screen):
    text_font = pygame.font.SysFont("comicsans", 30)
    utils.draw_text(screen, "Shall we play a game?", text_font, (0, 0, 0), 500, 100)

#method to switch between menus
def switchMenus(menu):
    utils.current_menu = menu

def initSelectMenu(screen):
    utils.clear_objects()
    drawMenuText(screen)

    utils.current_menu = "gameSelect"
    text_font = pygame.font.SysFont("comicsans", 30)

    # Buttons init
    pongButton = Button(
        screen, 425, 480, 150, 60, text='Pong', font=text_font,
        fontSize=50, margin=20,
        inactiveColour=(150, 150, 150),
        hoverColour=(100, 100, 100),
        pressedColour=(180, 180, 180),
        onClick=lambda: print("Play Pong!")
    )

    buttons = [pongButton]
    textObjects = []
    menuObjects = buttons + textObjects

    for object in menuObjects:
        object.setX(int(object.getX() * utils.scaleX))
        object.setY(int(object.getY() * utils.scaleY))
        object.setWidth(int(object.getWidth() * utils.scaleX))
        object.setHeight(int(object.getHeight() * utils.scaleY))
        utils.current_menu_objects.append(object)