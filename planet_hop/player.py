from pygame import Surface
from pygravity.twod import GravityContainer

from planet_hop import globals
from planet_hop.object import Object
from planet_hop.small_object import *
from planet_hop.planet import Planet
from planet_hop.pgimports import *

# isort: off
# These have duplicate names from above and need to override them
from planet_hop import constants
from pygravity.twod import Vector2 as GravVector2
# isort: on


MOVEMENT_SPEED = 10
JUMP_SPEED = 150
JUMP_TIME = 5


class Player(SmallObject):
    jump_time: float

    def __init__(self, container: GravityContainer):
        super().__init__(container, GravVector2(-149_600_000_000, 6_371_010), 70, 1, (0, 0, 255))
        self.jump_time = 0
        self.on_ground = False

    def step(self, time_passed: float) -> tuple[Vector2, Vector2]:
        dv, movement = super().step(time_passed)
        if K_a in globals.pressed_keys:
            self.physics.velocity += Vector2(MOVEMENT_SPEED, 0).rotate(-globals.rotation) * time_passed
        if K_d in globals.pressed_keys:
            self.physics.velocity += Vector2(-MOVEMENT_SPEED, 0).rotate(-globals.rotation) * time_passed
        if self.jump_time > 0 and K_SPACE in globals.pressed_keys:
            self.physics.velocity += Vector2(0, JUMP_SPEED).rotate(-globals.rotation) * time_passed
        self.on_ground = False
        for planet in globals.planets:
            rel: GravVector2 = self.position - planet.position
            dir, dist = rel.as_direction_magnitude()
            if dist < 1 + planet.radius:
                self.on_ground = True
                self.jump_time = JUMP_TIME
                self.position.set_to(*(planet.position + GravVector2.from_direction_magnitude(dir, 1 + planet.radius)))
                self.physics.velocity.set_to(*evaluate_friction(self.physics.velocity, self.closest.physics.velocity, GROUND_FRICTION, time_passed))
            elif dist < 1 + planet.atmosphere:
                self.physics.velocity.set_to(*evaluate_friction(self.physics.velocity, self.closest.physics.velocity, AIR_FRICTION, time_passed))
                self.jump_time -= 1
        self.update_closest()
        return dv, movement
