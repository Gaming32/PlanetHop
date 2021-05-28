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


class Player(Object):
    def __init__(self, container: GravityContainer):
        super().__init__(container, GravVector2(), 70)

    def step(self, time_passed: float) -> tuple[Vector2, Vector2]:
        result = super().step(time_passed)
        for planet in globals.planets:
            rel: GravVector2 = (self.position - planet.position)
            dir, dist = rel.as_direction_magnitude()
            if dist < 1 + planet.radius:
                self.position.set_to(*(planet.position + GravVector2.from_direction_magnitude(dir, 1 + planet.radius)))
        return result

    def render(self, surf: Surface):
        globals.camera += (self.position - globals.camera) * constants.CAMERA_LERP * globals.delta
        super().render(surf, 1, (0, 0, 255))
