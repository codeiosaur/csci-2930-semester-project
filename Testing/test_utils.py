import pytest
import pygame
import Menus.utils as utils

def test_getScreenDims():
    pygame.init() # Needed for getScreenDims to work
    utils.getScreenDims()
    screenInfo = pygame.display.Info()
    assert utils.REF_DIMS == (1000, 800), "REF_DIMS not match expected value"
    assert utils.screenWidth == screenInfo.current_w, "utils.screenWidth does not match resolution!"
    assert utils.screenHeight == screenInfo.current_h, "utils.screenHeight does not match resolution!"
    pygame.quit()

# The following tests all require some form of display to work properly.
# This is a helper function so that all the common initialization code is in one place.
def _screenTestHelper(caption):
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_caption(caption)
    utils.getScreenDims()
    screen = pygame.display.set_mode((utils.screenWidth, utils.screenHeight))
    return screen

# utils.draw_text relies on graphics that we can't test directly,
# so we test the logic instead.
def test_draw_text():
    screen = _screenTestHelper("Testing Draw Text")
    text_font = pygame.font.SysFont("menlo", 30)
    textX = 500; textY = 400 # text coordinates
    coords = utils.draw_text(screen, "Shall we do a test?", text_font,
                             (0, 0 ,0), textX, textY)
    assert coords[0] == int(500 * utils.scaleX), f"Expected {textX} * utils.scaleX, got {coords[0]}"
    assert coords[1] == int(400 * utils.scaleY), f"Expected {textY} * utils.scaleX, got {coords[1]}"

def test_widgets():
    from pygame_widgets.button import Button
    screen = _screenTestHelper("Testing Buttons")
