import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

print(pygame.font.get_fonts())
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

text_font = pygame.font.SysFont("comicsans", 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text,True,text_col)
    screen.blit(img, (x,y))

run = True
while run:

    screen.fill((255,255,255))

    draw_text("im crine", text_font, (255,0,255), 200, 100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
