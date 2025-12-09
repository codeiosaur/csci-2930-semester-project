import pygame
import Menus.utils as utils
from pygame_widgets.button import Button

def drawMenuText(screen):
    # Draw game over text
    text_font = pygame.font.SysFont("menlo", 45)
    winner = utils.previous_winner
    if winner is True:
        utils.draw_text(screen, "You Win!", text_font,
                        (25, 255, 25), 500, 200)
    elif winner is False:
        utils.draw_text(screen, "Game Over!", text_font,
                        (255, 25, 25), 500, 200)
    else:
        utils.draw_text(screen, "Game Ended.", text_font,
                        (255, 255, 255), 500, 200)

def restartPrevGame(screen):
    utils.clear_objects()
    if utils.previous_game is None:
       return # no previous game played
    elif utils.previous_game == "Pong":
        from Menus.gameSelect import startPong
        startPong(screen)


def initGameOverMenu(screen):
    screenInfo = utils.getScreenDims()
    utils.clear_objects()
    screen.fill((0, 0, 0))
    drawMenuText(screen)

    utils.switchMenus("gameOver")
    text_font = pygame.font.SysFont("menlo", 45)

    restart_button = Button(
        screen,350, 350, 300, 80,
        text='Play Again', font = text_font,
        fontSize=50, margin=20,
        inactiveColour=(0, 200, 0),
        hoverColour=(0, 150, 0),
        pressedColour=(0, 220, 0),
        onClick=lambda: restartPrevGame(screen)
    )

    select_button = Button(
        screen,350, 450, 300, 80,
        text='Other Games', font = text_font,
        fontSize=50, margin=20,
        inactiveColour=(225, 200, 0),
        hoverColour=(200, 175, 0),
        pressedColour=(255, 225, 0),
        onClick=lambda: utils.switchMenus("gameSelect")
    )

    menu_button = Button(
        screen,350, 550, 300, 80,
        text='Exit to Menu', font = text_font,
        fontSize=50, margin=20,
        inactiveColour=(150, 150, 150),
        hoverColour=(100, 100, 100),
        pressedColour=(180, 180, 180),
        onClick=lambda: utils.switchMenus("main")
    )

    buttons = [restart_button, select_button, menu_button]
    for button in buttons:
        button.setX(int(button.getX() * screenInfo["scaleX"]))
        button.setY(int(button.getY() * screenInfo["scaleY"]))
        button.setWidth(int(button.getWidth() * screenInfo["scaleX"]))
        button.setHeight(int(button.getHeight() * screenInfo["scaleY"]))
        utils.register_widget(button)