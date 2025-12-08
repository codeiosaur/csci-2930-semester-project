import pygame
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import Menus.utils as utils
from Games import Pong

def initSelectMenu(screen):
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

    # Text init
    prompt = TextBox(
        screen, int(460), int(100),
        int(400), int(400),
        fontSize=int(50),
        colour=(255, 255, 255),
        textColour=(0, 0, 0),
        borderThickness=0,
        isEditable=False
    )
    prompt.setText("Shall we play a game?")

    buttons = [pongButton]
    textObjects = [prompt]
    menuObjects = buttons + textObjects

    for object in menuObjects:
        object.setX(int(object.getX() * utils.scaleX))
        object.setY(int(object.getY() * utils.scaleY))
        object.setWidth(int(object.getWidth() * utils.scaleX))
        object.setHeight(int(object.getHeight() * utils.scaleY))
        utils.current_menu_objects.append(object)