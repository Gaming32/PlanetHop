from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygravity.twod import GravityContainer

    from planet_hop.pgimports import *
    from planet_hop.player import Player
    from planet_hop.types import Coroutine

screen: Surface
win_size: Rect
fullscreen: bool

container: GravityContainer
player: Player

camera_offset: Vector2
camera: Vector2
zoom: float

delta: float
coroutines: list[Coroutine]
