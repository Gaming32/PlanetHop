from pygame import Surface
from pygravity.twod import GravityContainer, Vector2

from planet_hop import constants, globals
from planet_hop.pgimports import *
from planet_hop.physics_applied import PhysicsApplied


class Object(PhysicsApplied):
    def render(self, surf: Surface, radius: float):
        pygame.draw.circle(
            surf,
            (0, 0, 255),
            (self.position - globals.camera) * globals.zoom + globals.camera_offset,
            radius * globals.zoom)
