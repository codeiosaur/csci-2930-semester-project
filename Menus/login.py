import pygame
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import Menus.utils as utils
import Data.DatabaseManager as db
from Menus.utils import switchMenus

loggingIn = False
exceptionText = "Please enter a valid username and password!"
exception = False

def drawMenuText(screen):
    text_font = pygame.font.SysFont("arial", 30)
    utils.draw_text(screen, "Login or Create account", text_font, (0, 0, 0), 400, 100)
    drawExceptionText(screen)


def setException():
    global exception
    exception = True

def drawExceptionText(screen):

    if exception == True:
        text_font = pygame.font.SysFont("arial", 15)
        utils.draw_text(screen, f"{exceptionText}", text_font, (255, 0, 0), 450, 400)

def login(screen, username, password):
    base = db.DatabaseManager()
    if username != '' and password != '' and base.usernameExists(username):
        Id = base.getIdFromName(username)
        if base.checkPassword(password,Id):
            utils.userId = Id
            login.loggingIn = False
            switchMenus("main")
        else:
            setException()
    else:
        setException()


def createAccount(screen, username,password):
    base = db.DatabaseManager()
    if username != '' and password != '':
        if not base.usernameExists(username):
            base.addUser(username,password)
            Id = base.getIdFromName(username)
            utils.userId = Id
            login.loggingIn = False
            switchMenus("main")
        else:
            setException()
    else:
        setException()

def initLoginMenu(screen):
    screenInfo = utils.getScreenDims()
    utils.clear_objects()

    drawMenuText(screen)
    utils.switchMenus("login")

    login.loggingIn = True
    # Other initializations (non-button)
    text_font = pygame.font.SysFont("arial", 30)
    pygame.display.set_caption("Main Window")

    usernameBox = TextBox(screen, 375, 200, 250, 80, placeholderText="Username:",
                          fontSize=50, font=text_font,
                          borderThickness=2, borderColour=(50,50,50))

    passwordBox = TextBox(screen, 375, 300, 250, 80, placeholderText="Password:",
                          fontSize=50, font=text_font,
                          borderThickness=2, borderColour=(50, 50, 50))

    loginButton = Button(
        screen, 500, 480, 150, 60, text='Log in', font= text_font,
        fontSize=50, margin=20,
        inactiveColour=(150, 150, 150),
        hoverColour=(100,100,100),
        pressedColour=(180, 180, 180),
        onClick=lambda: login(screen, usernameBox.getText(),passwordBox.getText())
    )

    createAccountButton = Button(
        screen, 350, 480, 150, 60, text='Create account', font=text_font,
        fontSize=50, margin=20,
        inactiveColour=(150, 150, 150),
        hoverColour=(100, 100, 100),
        pressedColour=(180, 180, 180),
        onClick=lambda: createAccount(screen, usernameBox.getText(), passwordBox.getText())
    )

    buttons = [ loginButton, createAccountButton]
    textObjects = [usernameBox,passwordBox]
    menuObjects = buttons + textObjects

    # Object resizing (only done once - no future resizing)
    for object in menuObjects:
        object.setX(int(object.getX() * screenInfo["scaleX"]))
        object.setY(int(object.getY() * screenInfo["scaleY"]))
        object.setWidth(int(object.getWidth() * screenInfo["scaleX"]))
        object.setHeight(int(object.getHeight() * screenInfo["scaleY"]))
        utils.register_widget(object)
