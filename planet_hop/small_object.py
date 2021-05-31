from pygame import Surface
from pygravity.twod import GravityContainer

from planet_hop import globals
from planet_hop.object import Object
from planet_hop.planet import Planet
from planet_hop.pgimports import *

# isort: off
# These have duplicate names from above and need to override them
from planet_hop import constants
from pygravity.twod import Vector2 as GravVector2
# isort: on


GROUND_FRICTION = 51.0
AIR_FRICTION = 50.3


def evaluate_friction(v1: GravVector2, v2: GravVector2, f: float, t: float):
    return (v1 - v2) / (f * t) + v2


class SmallObject(Object):
    closest: Planet
    rel: GravVector2
    radius: float
    color: Color
    on_ground: bool

    def __init__(self, container: GravityContainer, positon: Vector2, mass: float, radius: float, color: Color):
        super().__init__(container, positon, mass)
        self.radius = radius
        self.color = color
        self.on_ground = False

    def step(self, time_passed: float) -> tuple[Vector2, Vector2]:
        dv, movement = super().step(time_passed)
        self.on_ground = False
        for planet in globals.planets:
            rel: GravVector2 = self.position - planet.position
            dir, dist = rel.as_direction_magnitude()
            if dist < self.radius + planet.radius:
                self.on_ground = True
                self.position.set_to(*(planet.position + GravVector2.from_direction_magnitude(dir, self.radius + planet.radius)))
                self.physics.velocity.set_to(*evaluate_friction(self.physics.velocity, self.closest.physics.velocity, GROUND_FRICTION, time_passed))
            elif dist < self.radius + planet.atmosphere:
                self.physics.velocity.set_to(*evaluate_friction(self.physics.velocity, self.closest.physics.velocity, AIR_FRICTION, time_passed))
        self.update_closest()
        return dv, movement

    def closest_planet(self) -> Planet:
        return min(
            globals.planets,
            key=(lambda p: (p.position - globals.player.position).sqr_magnitude())
        )

    def update_closest(self):
        self.closest = self.closest_planet()
        self.rel = self.position - self.closest.position

    def post_init(self):
        self.update_closest()

    def render(self, surf: Surface):
        super().render(surf, self.radius, self.color)
