import pygame
import pygame_widgets
from Menus import mainMenu, gameSelect, login
from Menus import utils as utils

def main():
    pygame.init()

    # Setting screen constants
    screenInfo = utils.getScreenDims()

    print(pygame.font.get_fonts())

    # Create the screen.
    # scale_x = scale_y = 1
    # screen = pygame.display.set_mode((1000, 800))
    screen = pygame.display.set_mode((screenInfo["width"], screenInfo["height"]))

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
                        utils.current_menu = "main"

        # Draw text
        if utils.current_menu == "main":
            mainMenu.drawMenuText(screen)
        elif utils.current_menu == "gameSelect":
            gameSelect.drawMenuText(screen)
        elif utils.current_menu == "login":
            login.initLoginMenu(screen)

        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()