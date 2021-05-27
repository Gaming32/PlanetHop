from pygame import Surface
from pygravity.twod import GravityContainer

from planet_hop import globals
from planet_hop.object import Object
from planet_hop.pgimports import *

# isort: off
# These have duplicate names from above and need to override them
from planet_hop import constants
from pygravity.twod import Vector2
# isort: on


class Player(Object):
    def __init__(self, container: GravityContainer):
        super().__init__(container, Vector2(), 70)

    def render(self, surf: Surface):
        globals.camera = globals.camera.lerp(self.position, constants.CAMERA_LERP)
        super().render(surf, 1)
