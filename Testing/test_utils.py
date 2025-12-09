import pytest
import pygame
import Menus.utils as utils

def test_getScreenDims():
    pygame.init() # Needed for getScreenDims to work
    utils.getScreenDims()
    screenInfo = pygame.display.Info()
    assert utils.REF_DIMS == (1000, 800), "REF_DIMS not match expected value"
    assert utils.screenWidth == screenInfo.current_w, "screenWidth does not match resolution!"
    assert utils.screenHeight == screenInfo.current_h, "screenHeight does not match resolution!"
    pygame.quit()