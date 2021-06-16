import threading
import time


from threading import Timer
import time


class Timer:

    def __init__(self):
        self.startTime = None
        self.cancelTime = None
        self.currentTime = None
        self.isPaused = False

    def start(self):
        self.startTime = time.time()

    def pause(self):
        self.currentTime = time.time() - self.startTime
        self.cancelTime = self.currentTime
        self.isPaused = True
        return self.currentTime

    def getTime(self):
        if self.cancelTime == None:
            self.currentTime = time.time() - self.startTime
        else:
            self.currentTime = time.time() - self.startTime + self.cancelTime
        return self.currentTime

    def resume(self):
        self.starTime = time.time()
        self.isPaused = False
