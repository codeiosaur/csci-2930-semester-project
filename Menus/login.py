import pygame
import pygame_widgets
from pygame_widgets.button import Button
def initLoginMenu():
    pygame.init()

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800

    print(pygame.font.get_fonts())
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    text_font = pygame.font.SysFont("comicsans", 30)
    bg_color = (255, 255, 255)
    pygame.display.set_caption("Main Window")

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    running = True

    while running:

        screen.fill(bg_color)

        draw_text("pmo", text_font, (255, 0, 255), 430, 100)
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