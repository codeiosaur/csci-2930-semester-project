import pygame
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import Menus.utils as utils


def drawMenuText(screen):
    text_font = pygame.font.SysFont("comicsans", 30)
    utils.draw_text(screen, "Login or Sign up", text_font, (0, 0, 0), 500, 100)

#method to switch between menus
def switchMenus(menu):
    utils.current_menu = menu

def initLoginMenu(screen):
    utils.clear_objects()
    drawMenuText(screen)

    utils.current_menu = "login"

    # Other initializations (non-button)
    text_font = pygame.font.SysFont("comicsans", 30)
    pygame.display.set_caption("Main Window")

    usernameBox = TextBox(screen, 375, 200, 250, 80, placeholderText="Username:",
                          fontSize=50, font=text_font,
                          borderThickness=2, borderColour=(50,50,50))

    settingsButton = Button(
        screen, 425, 480, 150, 60, text='Settings', font= text_font,
        fontSize=50, margin=20,
        inactiveColour=(150, 150, 150),
        hoverColour=(100,100,100),
        pressedColour=(180, 180, 180),
        onClick=lambda: print('Click')
    )
    buttons = [ settingsButton]
    textObjects = [usernameBox]
    menuObjects = buttons + textObjects

    # Object resizing (only done once - no future resizing)
    for object in menuObjects:
        object.setX(int(object.getX() * utils.scaleX))
        object.setY(int(object.getY() * utils.scaleY))
        object.setWidth(int(object.getWidth() * utils.scaleX))
        object.setHeight(int(object.getHeight() * utils.scaleY))
        utils.current_menu_objects.append(object)