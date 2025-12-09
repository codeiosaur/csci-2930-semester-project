import pygame

current_menu_objects = []
current_menu = None

REF_DIMS = (1000, 800) # Reference width, reference height

screenWidth, screenHeight = None, None
scaleX, scaleY = None, None

# Set global variables regarding the screen resolution.
# Must have called pygame.init() before calling this function.
def getScreenDims():
    global screenWidth, screenHeight, scaleX, scaleY, current_menu, REF_DIMS
    info = pygame.display.Info()
    screenWidth = info.current_w
    screenHeight = info.current_h
    scaleX = screenWidth / REF_DIMS[0]
    scaleY = screenHeight / REF_DIMS[1]

# Function that draws text.
# Does NOT automatically handle scaling, this must be done by the function caller.
def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(int(x * scaleX), int(y * scaleY)))
    screen.blit(img, text_rect)
    return (int(x * scaleX), int(y * scaleY))

# Remove all objects i.e. widgets (used to switch menus)
def clear_objects():
    global current_menu_objects
    for object in current_menu_objects:
        object.hide()

# Add widget to tracking list
def register_widget(widget):
    current_menu_objects.append(widget)
    return widget