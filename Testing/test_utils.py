import pytest
import pygame
import Menus.utils as utils

# Some tests require some form of display to work properly.
# This is a helper function so that all the common initialization code is in one place.
def _screenTestHelper(caption):
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    screenInfo = utils.getScreenDims()
    if pygame.get_init():
        return pygame.display.set_mode((screenInfo["width"], screenInfo["height"]))
    else:
        pygame.init()
        pygame.display.set_caption(caption)
        screen = pygame.display.set_mode((screenInfo["width"], screenInfo["height"]))
        return screen

# Helper method used for various widget tests
def _initButtons(screen, text_font):
    from pygame_widgets.button import Button
    # Buttons init
    button1 = Button(
        screen, 100, 100, 250, 150, text='button1', font=text_font,
        fontSize=50, margin=20,
        inactiveColour=(0, 200, 0),
        hoverColour=(0, 150, 0),
        pressedColour=(0, 220, 0),
        onClick=lambda: print("button1")
    )
    button2 = Button(
        screen, 500, 100, 250, 150, text='button2', font=text_font,
        fontSize=50, margin=20,
        inactiveColour=(0, 200, 0),
        hoverColour=(0, 150, 0),
        pressedColour=(0, 220, 0),
        onClick=lambda: print("button2")
    )

    button3 = Button(
        screen, 600, 400, 350, 350, text='button3', font=text_font,
        fontSize=50, margin=20,
        inactiveColour=(0, 200, 0),
        hoverColour=(0, 150, 0),
        pressedColour=(0, 220, 0),
        onClick=lambda: print("button3")
    )

    buttons = [button1, button2, button3]
    origCoords = [] # unscaled coordinates
    origDims = [] # unscaled dimensions
    for button in buttons:
        origCoords.append((button.getX(), button.getY()))
        origDims.append((button.getWidth(), button.getHeight()))

    return (buttons, origCoords, origDims)

def test_getScreenDims():
    pygame.init() # Needed for getScreenDims to work
    originalInfo = pygame.display.Info()
    newInfo = utils.getScreenDims()
    assert newInfo["width"] == originalInfo.current_w,\
        "screenWidth does not match resolution!"
    assert newInfo["height"] == originalInfo.current_h, \
        "screenHeight does not match resolution!"
    pygame.quit()

# utils.draw_text relies on graphics that we can't test directly,
# so we test the logic instead.
def test_draw_text():
    screen = _screenTestHelper("Testing Draw Text")
    screenInfo = utils.getScreenDims()
    text_font = pygame.font.SysFont("menlo", 30)
    textX = 500; textY = 400 # text coordinates
    coords = utils.draw_text(screen, "Shall we do a test?", text_font,
                             (0, 0 ,0), textX, textY)
    assert coords[0] == int(500 * screenInfo["scaleX"]), f"Expected {textX * screenInfo["scaleX"]}, got {coords[0]}"
    assert coords[1] == int(400 * screenInfo["scaleY"]), f"Expected {textY * screenInfo["scaleY"]}, got {coords[1]}"

def test_register_widget():
    screen = _screenTestHelper("Testing Buttons")
    text_font = pygame.font.SysFont("arialunicode", 30)
    buttons = _initButtons(screen, text_font)[0]

    for object in buttons:
        utils.register_widget(object)

    assert buttons[0] in utils.current_menu_objects
    assert buttons[1] in utils.current_menu_objects
    assert buttons[2] in utils.current_menu_objects

    utils.clear_objects()

def test_widget_scaling():
    screenInfo = utils.getScreenDims()
    screen = _screenTestHelper("Testing Buttons")
    text_font = pygame.font.SysFont("arialunicode", 30)
    buttons, origCoords, origDims = _initButtons(screen, text_font)

    for object in buttons:
        object.setX(int(object.getX() * screenInfo["width"]))
        object.setY(int(object.getY() * screenInfo["height"]))
        object.setWidth(int(object.getWidth() * screenInfo["width"]))
        object.setHeight(int(object.getHeight() * screenInfo["height"]))
        utils.register_widget(object)

    epsilon = 0.5
    for i in range(len(buttons)):
        # Because of rounding when setting the coordinates, if we try to compare
        # the scaled and original coordinates directly the tests would fail.
        # So we simply check if they are close to each other instead.
        assert abs(buttons[i].getX() / screenInfo["width"] - origCoords[i][0]) < epsilon,\
            f"button{i}.X = {buttons[i].getX()}"
        assert abs(buttons[i].getY() / screenInfo["height"] - origCoords[i][1]) < epsilon, \
            f"button{i}.Y = {buttons[i].getY()}"
        assert abs(buttons[i].getWidth() / screenInfo["width"] - origDims[i][0]) < epsilon, \
            f"button{i}.X = {buttons[i].getX()}"
        assert abs(buttons[i].getHeight() / screenInfo["height"] - origDims[i][1]) < epsilon, \
            f"button{i}.Y = {buttons[i].getY()}"