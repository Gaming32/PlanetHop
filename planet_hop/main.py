import math as pymath
from planet_hop.bounce import Bouncy
from planet_hop.small_object import SmallObject

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
globals.planets = [
    Planet(globals.container, GravVector2(0, 0), 1.989e30, 696_340_000, (252, 150, 1)),
    Planet(globals.container, GravVector2(-149_600_000_000, 0), 5.972e+24, 6_371_000, (86, 176, 0), 6_400_000, (135, 206, 235)),
]
globals.planets[1].physics.add_velocity_vector(GravVector2(0, -30000)) # Earth
globals.objects = [
    globals.player,
    Bouncy(globals.container, GravVector2(-149_600_000_005, 6_371_010), 70, 1, (255, 0, 0)),
]
for object_ in globals.objects:
    object_.post_init()

globals.camera_offset = Vector2(*globals.view_size.size) / 2
globals.camera = Vector2(globals.player.position)
globals.zoom = 10
globals.freecam = False

globals.pressed_keys = set()
globals.coroutines = []


def get_box_offset() -> Vector2:
    return -1 * (globals.camera_offset - Vector2(globals.win_size.size) / 2)


def get_rotation() -> float:
    return -(globals.player.closest.position - globals.player.position).direction() - 90


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
            globals.pressed_keys.add(event.key)
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
            elif event.key == K_F12:
                globals.freecam = not globals.freecam
                if not globals.freecam:
                    globals.camera_offset = Vector2(*globals.view_size.size) / 2
        elif event.type == KEYUP:
            globals.pressed_keys.discard(event.key)
        elif event.type == VIDEORESIZE:
            globals.win_size = screen.get_rect()
            box_offset = get_box_offset()

    render_box.fill((0, 0, 0))

    if globals.freecam:
        if K_UP in globals.pressed_keys:
            globals.camera_offset.y += 200 * delta
        if K_DOWN in globals.pressed_keys:
            globals.camera_offset.y -= 200 * delta
        if K_LEFT in globals.pressed_keys:
            globals.camera_offset.x += 200 * delta
        if K_RIGHT in globals.pressed_keys:
            globals.camera_offset.x -= 200 * delta
        if K_KP0 in globals.pressed_keys:
            globals.zoom /= pow(5, delta)
        if K_KP1 in globals.pressed_keys:
            globals.zoom *= pow(5, delta)

    for planet in globals.planets:
        planet.update(delta)
    for object_ in globals.objects:
        object_.update(delta)

    globals.camera.update(globals.player.position)
    for planet in globals.planets:
        planet.render(render_box)
    for object_ in globals.objects:
        object_.render(render_box)

    preferred_rotation = get_rotation()
    rot_delta = (preferred_rotation - globals.rotation + 180) % 360 - 180
    rot_delta = max(min(rot_delta, ROTATION_SPEED_MAX), -ROTATION_SPEED_MAX) + max(min(rot_delta, ROTATION_SPEED_MIN), -ROTATION_SPEED_MIN)
    globals.rotation += rot_delta * delta
    print(f'{clock.get_fps():6.2f}  {globals.player.position}  {globals.player.physics.velocity}', end='\r')
    # print(f'{clock.get_fps():6.2f}  {globals.planets[1].position}  {globals.planets[1].physics.velocity}', end='\r')
    screen.blit(render_box, box_offset)

    pygame.display.update()


print()
