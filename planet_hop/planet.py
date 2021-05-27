from pygame import Rect, Surface
from pygame.locals import Color
from pygravity.twod.gravity import GravityContainer
from pygravity.twod.vector import Vector2
from planet_hop.object import Object
from planet_hop import globals


class Planet(Object):
    radius: float
    color: Color

    def __init__(self, container: GravityContainer, positon: Vector2, mass: float, radius: float, color: Color):
        super().__init__(container, positon, mass)
        self.radius = radius
        self.color = color

    # def step(self, time_passed: float) -> tuple[Vector2, Vector2]:
    #     print(type(self.position), end=' ')
    #     super().step(time_passed)
    #     print(type(self.position))

    def render(self, surf: Surface):
        render_radius = self.radius * globals.zoom
        if render_radius > 1_000_000:
            center: Vector2 = (globals.camera - self.position) * globals.zoom + globals.camera_offset
            dims = surf.get_rect()
            left = max(-20, center.x - render_radius)
            right = min(center.x + render_radius, dims.width + 20)
            top = max(-20, center.y - render_radius)
            bottom = min(center.y + render_radius, dims.height + 20)
            surf.fill(self.color, Rect(left, top, right - left, bottom - top))
        else:
            super().render(surf, self.radius, self.color)
