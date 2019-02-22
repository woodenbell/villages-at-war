from threading import Semaphore


class Barrier(object):
    ...

    def __init__(self, n: int):
        self.n = None # type: int
        self.count = None # type: int
        self.mutex = None # type: Semaphore
        self.barrier = None # type: Semaphore
        ...

    def wait(self): ...

    def release(self): ...
