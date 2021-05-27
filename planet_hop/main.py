from planet_hop import constants as globals
from planet_hop.pgimports import *
from planet_hop.constants import *

pygame.init()

winfo = pygame.display.Info()
screen = pygame.display.set_mode((1280, 720), SCREEN_FLAGS)
globals.screen = screen
globals.win_size = screen.get_rect()
globals.fullscreen = False

globals.coroutines = []


clock = pygame.time.Clock()
running = True

while running:
    ms = clock.tick(75)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_F11:
                globals.fullscreen = not globals.fullscreen
                if globals.fullscreen:
                    pygame.display.quit()
                    screen = pygame.display.set_mode((winfo.current_w, winfo.current_h), SCREEN_FLAGS | FULLSCREEN)
                else:
                    pygame.display.quit()
                    screen = pygame.display.set_mode((1280, 720), SCREEN_FLAGS)
                globals.screen = screen
                globals.win_size = screen.get_rect()
        elif event.type == VIDEORESIZE:
            globals.win_size = screen.get_rect()

    print(globals.win_size)
    pygame.display.update()
