import pygame
import pygame_widgets
from Menus import mainMenu
from Menus import utils as utils

def main():
    pygame.init()

    # Setting screen constants
    utils.getScreenDims()

    # Create the screen.
    # scale_x = scale_y = 1
    # screen = pygame.display.set_mode((1000, 800))
    screen = pygame.display.set_mode((utils.screenWidth, utils.screenHeight))

    # Initialize main menu
    utils.current_menu = "main"
    mainMenu.initMainMenu(screen)

    # Final init
    running = True
    bg_color = (255, 255, 255)
    clock = pygame.time.Clock()

    while running:
        screen.fill(bg_color)
        # event handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if utils.current_menu == "main":
                        running = False  # Quit from main menu
                    elif utils.current_menu == "gameSelect":
                        # Go back to main menu
                        mainMenu.initMainMenu(screen)

        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()