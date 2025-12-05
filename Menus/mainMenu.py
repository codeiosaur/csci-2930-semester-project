import pygame
import pygame_widgets
from pygame_widgets.button import Button

pygame.init()

# unused
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

print(pygame.font.get_fonts())
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
text_font = pygame.font.SysFont("comicsans", 30)
bg_color = (255, 255, 255)
pygame.display.set_caption("Main Window")

def draw_text(text, font, text_col, x, y):
    img = font.render(text,True,text_col)
    screen.blit(img, (x,y))

startButton = Button(
    screen, 000, 100, 300, 150, text='login',
    fontSize=50, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0),
    onClick=lambda: print('Click')
)

def initMainMenu():
    running = True

    while running:

        screen.fill(bg_color)

        draw_text("im crime", text_font, (255,0,255), 200, 100)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame_widgets.update(events)
        pygame.display.flip()

    pygame.quit()
