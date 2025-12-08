import pygame

current_menu_objects = []
current_menu = None

REF_DIMS = (1000, 800) # Reference width, reference height

screenWidth, screenHeight = None, None
scaleX, scaleY = None, None

# Get and return two tuples: the screen resolution and the correct scale factor.
# Must have called pygame.init() before calling this function.
def getScreenDims():
    global screenWidth, screenHeight, scaleX, scaleY, current_menu
    info = pygame.display.Info()
    screenWidth = info.current_w
    screenHeight = info.current_h
    scaleX = screenWidth / REF_DIMS[0]
    scaleY = screenHeight / REF_DIMS[1]
    # REF_DIMS = (1000, 800)  # Reference width, reference height
    # SCREEN_INFO = pygame.display.Info()
    # return {
    #     'width': SCREEN_INFO.current_w,
    #     'height': SCREEN_INFO.current_h,
    #     'scale_x': SCREEN_INFO.current_w / REF_DIMS[0],
    #     'scale_y': SCREEN_INFO.current_h / REF_DIMS[1]
    # }

# Function that draws text.
# Does NOT automatically handle scaling, this must be done by the function caller.
def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Remove all objects i.e. widgets (used to switch menus)
def clear_objects():
    global current_menu_objects
    for object in current_menu_objects:
        object.hide()
    current_objects = []

# Add widget to tracking list
def register_widget(widget):
    current_menu_objects.append(widget)
    return widget