from planet_hop.planet import Planet
from pygravity.twod.gravity import GravityCaster, GravityContainer

from planet_hop import globals
from planet_hop.constants import *
from planet_hop.pgimports import *
from planet_hop.player import Player
from pygravity.twod import Vector2 as GravVector2

pygame.init()

winfo = pygame.display.Info()
screen = pygame.display.set_mode((1280, 720), SCREEN_FLAGS)
pygame.display.set_caption(GAME_TITLE)
globals.screen = screen
globals.win_size = screen.get_rect()
globals.fullscreen = False

globals.container = GravityContainer()
globals.player = Player(globals.container)
globals.planets = [Planet(globals.container, GravVector2(0, -6_371_010), 5.972e+24, 6_371_000, (0, 255, 0))]

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

    for planet in globals.planets:
        planet.update(delta)
        planet.render(screen)

    globals.player.update(delta)
    globals.player.render(screen)

    pygame.display.update()
