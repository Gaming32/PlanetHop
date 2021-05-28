import math as pymath

from planet_hop.planet import Planet
from pygravity.twod.gravity import GravityCaster, GravityContainer

from planet_hop import globals
from planet_hop.constants import *
from planet_hop.pgimports import *
from planet_hop.player import Player
from pygravity.twod import Vector2 as GravVector2

pygame.init()

winfo = pygame.display.Info()
across = pymath.ceil(pymath.hypot(winfo.current_w, winfo.current_h))
globals.view_size = Rect(0, 0, across, across)

screen = pygame.display.set_mode((1280, 720), SCREEN_FLAGS)
pygame.display.set_caption(GAME_TITLE)
globals.screen = screen
globals.win_size = screen.get_rect()
globals.fullscreen = False

globals.container = GravityContainer()
globals.player = Player(globals.container)
globals.planets = [Planet(globals.container, GravVector2(0, -6_371_010), 5.972e+24, 6_371_000, (0, 255, 0))]

globals.camera_offset = Vector2(*globals.view_size.size) / 2
globals.camera = Vector2()
globals.zoom = 10

globals.coroutines = []


def get_box_offset() -> Vector2:
    return -1 * (globals.camera_offset - Vector2(globals.win_size.size) / 2)


def get_rotation() -> float:
    return (min(
            globals.planets,
            key=(lambda p: (p.position - globals.player.position).sqr_magnitude())
        ).position - globals.player.position).direction() + 90


render_box = Surface(globals.view_size.size)
box_offset = get_box_offset()


globals.rotation = get_rotation()


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


clock = pygame.time.Clock()
running = True

while running:
    # ms = clock.tick(75)
    ms = clock.tick()
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
                box_offset = get_box_offset()
        elif event.type == VIDEORESIZE:
            globals.win_size = screen.get_rect()
            box_offset = get_box_offset()

    render_box.fill((0, 0, 0))

    for planet in globals.planets:
        planet.update(delta)
        planet.render(render_box)

    globals.player.update(delta)
    globals.player.render(render_box)

    preferred_rotation = get_rotation()
    globals.rotation = (globals.rotation + (preferred_rotation - globals.rotation) * ROTATION_LERP * delta + 180) % 360 - 180
    print(f'{clock.get_fps():.2f}                      ', end='\r')
    screen.blit(render_box, box_offset)

    pygame.display.update()


print()
