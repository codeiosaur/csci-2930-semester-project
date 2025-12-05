import pygame
import pygame_widgets
from pygame_widgets.button import Button

def initMainMenu():
    pygame.init()

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800

    print(pygame.font.get_fonts())
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    text_font = pygame.font.SysFont("comicsans", 30)
    bg_color = (255, 255, 255)
    pygame.display.set_caption("Main Window")

    def draw_text(text, font, text_col, x, y):
        img = font.render(text,True,text_col)
        screen.blit(img, (x,y))





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

    running = True

    while running:

        screen.fill(bg_color)

        draw_text("im crine", text_font, (255, 0, 255), 430, 100)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame_widgets.update(events)
        pygame.display.flip()

    pygame.quit()


initMainMenu()


