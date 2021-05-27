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

    def render(self, surf: Surface):
        globals.camera += (self.position - globals.camera) * constants.CAMERA_LERP * globals.delta
        super().render(surf, 1, (0, 0, 255))
