import pygame
class Window:
    mainbg_color = (255, 255, 255)

    def display(self):
        pass
    def displayLeaderboard(self):
        pass
    def displayMain(self):
        print("entered main")
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Main Window")
        screen.fill(self.mainbg_color)
        pygame.display.flip()
        print("Main Run Successfully")
        return True
    def displayGame(self):
        pass
