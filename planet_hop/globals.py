from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygravity.twod import GravityContainer

    from planet_hop.pgimports import *
    from planet_hop.player import Player
    from planet_hop.planet import Planet
    from planet_hop.small_object import SmallObject
    from planet_hop.types import Coroutine

screen: Surface
win_size: Rect
fullscreen: bool

container: GravityContainer
player: Player
planets: list[Planet]
objects: list[SmallObject]

camera_offset: Vector2
view_size: Rect

camera: Vector2
zoom: float
rotation: float
freecam: bool

delta: float
pressed_keys: set[int]
coroutines: list[Coroutine]
