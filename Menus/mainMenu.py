import pygame
import pygame_widgets
from pygame_widgets.button import Button

# Get and return two tuples: the screen resolution and the correct scale factor.
# Must have called pygame.init() before calling this function.
def getScreenDims():
    REF_DIMS = (1000, 800)  # Reference width, reference height
    SCREEN_INFO = pygame.display.Info()
    SCREEN_DIMS = (SCREEN_INFO.current_w, SCREEN_INFO.current_h)
    return ((SCREEN_DIMS[0], SCREEN_DIMS[1]),
            (SCREEN_DIMS[0] / REF_DIMS[0], SCREEN_DIMS[1] / REF_DIMS[1]))

def initMainMenu():
    pygame.init()

    # Defining screen constants
    SCREEN_DIMS = getScreenDims()
    print(SCREEN_DIMS)
    scale_x = SCREEN_DIMS[1][0]
    scale_y = SCREEN_DIMS[1][1]

    # Create the screen.
    # SCREEN_DIMS[0] is the tuple containing the display width + height.
    # SCREEN_DIMS[1] contains the relevant scale factors.
    scale_x = scale_y = 1
    screen = pygame.display.set_mode((1000, 800))
    #screen = pygame.display.set_mode((SCREEN_DIMS[0][0], SCREEN_DIMS[0][1]))

    # Other initializations (non-button)
    text_font = pygame.font.SysFont("comicsans", 30)
    bg_color = (255, 255, 255)
    pygame.display.set_caption("Main Window")

    # Function that draws text. Automatically handles scaling.
    def draw_text(text, font, text_col, x, y):
        img = font.render(text,True,text_col)
        screen.blit(img, (x * scale_x, y * scale_y))

    # Buttons init
    startButton = Button(
        screen, 375, 250, 250, 150, text='Start', font= text_font,
        fontSize=50, margin=20,
        inactiveColour=(0, 200, 0),
        hoverColour=(0,150,0),
        pressedColour=(0, 220, 0),
        onClick=lambda: print('Click')
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

    # Button resizing (only done once - no future resizing)
    for button in buttons:
        button.setX(int(button.getX() * scale_x))
        button.setY(int(button.getY() * scale_y))
        button.setWidth(int(button.getWidth() * scale_x))
        button.setHeight(int(button.getHeight() * scale_y))

    # Main menu loop
    running = True
    while running:
        # background
        screen.fill(bg_color)

        # text
        draw_text("im crine", text_font, (255, 0, 255), 450, 100)

        # event handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        pygame_widgets.update(events)
        pygame.display.flip()

    pygame.quit()