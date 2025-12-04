import Window, pygame
def main():
    window = Window.Window()
    running = window.displayMain()
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for QUIT event
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()

if __name__ == '__main__':
    main()
