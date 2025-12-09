import pygame

current_menu_objects = []
current_menu = None
previous_game = None

# Set global variables regarding the screen resolution.
def getScreenDims():
    if not pygame.get_init():
        pygame.init()
    global current_menu
    REF_DIMS = (1000, 800)  # Reference width, reference height
    info = pygame.display.Info()
    return {
        "width": info.current_w,
        "height": info.current_h,
        "scaleX": info.current_w / REF_DIMS[0],
        "scaleY": info.current_h / REF_DIMS[1]
    }

# Function that draws text.
# Automatically handle display scaling for location but not font size.
def draw_text(screen, text, font, text_col, x, y):
    screenInfo = getScreenDims()
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(int(x * screenInfo["scaleX"]), int(y * screenInfo["scaleY"])))
    screen.blit(img, text_rect)
    return int(x * screenInfo["scaleX"]), int(y * screenInfo["scaleY"])

# Remove all objects i.e. widgets (used to switch menus)
def clear_objects():
    global current_menu_objects
    for object in current_menu_objects:
        object.hide()

# Add widget to tracking list
def register_widget(widget):
    current_menu_objects.append(widget)
    return widget

#method to switch between menus
def switchMenus(menu):
    global current_menu
    current_menu = menu

def setPreviousGame(game):
    global previous_game
    previous_game = game