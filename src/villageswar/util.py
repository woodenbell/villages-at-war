from builtins import object
from threading import Semaphore

# Python 2 compatible barrier


class Barrier(object):
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)

    def wait(self):
        self.mutex.acquire()
        self.count += 1
        self.mutex.release()
        
        if self.count == self.n:
            self.barrier.release()
            
        self.barrier.acquire()
        self.barrier.release()
    
    def release(self):
        self.barrier.release()
