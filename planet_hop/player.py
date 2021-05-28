from pygame import Surface
from pygravity.twod import GravityContainer

from planet_hop import globals
from planet_hop.object import Object
from planet_hop.pgimports import *

# isort: off
# These have duplicate names from above and need to override them
from planet_hop import constants
from pygravity.twod import Vector2 as GravVector2
# isort: on


MOVEMENT_SPEED = 10
JUMP_SPEED = 150
GROUND_FRICTION = 51.5
AIR_FRICTION = 50.1
JUMP_TIME = 5


class Player(Object):
    jump_time: float

    def __init__(self, container: GravityContainer):
        super().__init__(container, GravVector2(), 70)
        self.jump_time = 0

    def step(self, time_passed: float) -> tuple[Vector2, Vector2]:
        dv, movement = super().step(time_passed)
        if K_a in globals.pressed_keys:
            self.physics.velocity += Vector2(MOVEMENT_SPEED, 0).rotate(-globals.rotation) * time_passed
        if K_d in globals.pressed_keys:
            self.physics.velocity += Vector2(-MOVEMENT_SPEED, 0).rotate(-globals.rotation) * time_passed
        if self.jump_time > 0 and K_SPACE in globals.pressed_keys:
            self.physics.velocity += Vector2(0, JUMP_SPEED).rotate(-globals.rotation) * time_passed
        for planet in globals.planets:
            rel: GravVector2 = (self.position - planet.position)
            dir, dist = rel.as_direction_magnitude()
            if dist < 1 + planet.radius:
                self.jump_time = JUMP_TIME
                self.position.set_to(*(planet.position + GravVector2.from_direction_magnitude(dir, 1 + planet.radius)))
                # self.physics.velocity.set_to(*GravVector2.from_direction_magnitude(dir - 180, self.physics.velocity.magnitude() - FRICTION * globals.delta))
                self.physics.velocity /= GROUND_FRICTION * time_passed
            elif dist < 1 + planet.atmosphere:
                self.physics.velocity /= AIR_FRICTION * time_passed
                self.jump_time -= 1
        return dv, movement

    def render(self, surf: Surface):
        globals.camera += (self.position - globals.camera) * constants.CAMERA_LERP * globals.delta
        super().render(surf, 1, (0, 0, 255))
