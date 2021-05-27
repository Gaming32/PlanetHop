from pygravity.twod import GravityContainer, Vector2
from pygravity.twod.util import Body

PHYSICS_TICK_RATE: float = 50
physics_tick_time = 1 / PHYSICS_TICK_RATE


class PhysicsApplied(Body):
    passed: float

    def __init__(self, container: GravityContainer, positon: Vector2, mass: float):
        super().__init__(container, positon, mass)
        self.passed = 0

    def update(self, delta: float):
        self.passed += delta
        while self.passed > physics_tick_time:
            self.step(physics_tick_time)
            self.passed -= physics_tick_time
