from pygravity.twod.gravity import GravityContainer

from planet_hop import globals
from planet_hop.constants import *
from planet_hop.pgimports import *
from planet_hop.player import Player

pygame.init()

winfo = pygame.display.Info()
screen = pygame.display.set_mode((1280, 720), SCREEN_FLAGS)
pygame.display.set_caption(GAME_TITLE)
globals.screen = screen
globals.win_size = screen.get_rect()
globals.fullscreen = False

globals.container = GravityContainer()
globals.player = Player(globals.container)

globals.camera_offset = Vector2(*globals.win_size.size) / 2
globals.camera = Vector2()
globals.zoom = 10

globals.coroutines = []


clock = pygame.time.Clock()
running = True

while running:
    ms = clock.tick(75)
    globals.delta = delta = ms / 1000

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_F11:
                globals.fullscreen = not globals.fullscreen
                if globals.fullscreen:
                    pygame.display.quit()
                    screen = pygame.display.set_mode((winfo.current_w, winfo.current_h), SCREEN_FLAGS | FULLSCREEN)
                    pygame.display.set_caption(GAME_TITLE)
                else:
                    pygame.display.quit()
                    screen = pygame.display.set_mode((1280, 720), SCREEN_FLAGS)
                    pygame.display.set_caption(GAME_TITLE)
                globals.screen = screen
                globals.win_size = screen.get_rect()
                globals.camera_offset = Vector2(*globals.win_size.size) / 2
        elif event.type == VIDEORESIZE:
            globals.win_size = screen.get_rect()
            globals.camera_offset = Vector2(*globals.win_size.size) / 2

    screen.fill((0, 0, 0))

    globals.player.update(delta)
    globals.player.render(screen)

    pygame.display.update()
