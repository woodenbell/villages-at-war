from threading import Thread

from villageswar.util import Barrier
from villageswar.world import World


class WorldUpdater(Thread):
    ...

    def __init__(self, world, barrier):
        super().__init__()
        self.world_obj = None # type: World
        self.barrier = None # type: Barrier
        self.should_run = None # type: bool
        ...

    def run(self): ...

def main(): ...
