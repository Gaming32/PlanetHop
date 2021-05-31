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


class Bouncy(SmallObject):
    def step(self, time_passed: float) -> tuple[Vector2, Vector2]:
        res = super().step(time_passed)
        if self.on_ground:
            self.physics.velocity.set_to(*(
                (self.physics.velocity - self.closest.physics.velocity) * -1 + self.closest.physics.velocity)
            )
        return res
