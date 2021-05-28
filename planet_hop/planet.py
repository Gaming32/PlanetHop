from __future__ import annotations
from pygame import Rect, Surface
from pygame.locals import Color
from pygravity.twod.gravity import GravityContainer
from pygravity.twod.vector import Vector2 as GravVector2
from planet_hop.object import Object
from planet_hop import globals
from planet_hop.pgimports import *


class Planet(Object):
    radius: float
    color: Color
    atmosphere: float

    def __init__(self, container: GravityContainer, positon: GravVector2, mass: float, radius: float, color: Color, atmosphere: float):
        super().__init__(container, positon, mass)
        self.radius = radius
        self.color = color
        self.atmosphere = atmosphere

    def render(self, surf: Surface):
        render_radius = self.radius * globals.zoom
        if render_radius > 1_000_000:
            center: Vector2 = (globals.camera - self.position) * globals.zoom
            center.rotate_ip(round(globals.rotation / 90) * 90)
            center += globals.camera_offset
            dims = surf.get_rect()
            left = max(-20, center.x - render_radius)
            right = min(center.x + render_radius, dims.width + 20)
            top = max(-20, center.y - render_radius)
            bottom = min(center.y + render_radius, dims.height + 20)
            surf.fill(self.color, Rect(left, top, right - left, bottom - top))
        else:
            super().render(surf, self.radius, self.color)
