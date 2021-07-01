"""
Filename: timer.py
Version name: 0.1, 2021-05-21
Short description: Simple timer which can be paused

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
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
        self.isPaused = True
        self.currentTime = self.getTime()
        self.cancelTime = self.currentTime
        return self.currentTime

    def getTime(self):
        if self.cancelTime == None:
            self.currentTime = time.time() - self.startTime
        else:
            self.currentTime = time.time() - self.startTime + self.cancelTime
        return self.currentTime

    def resume(self):
        self.isPaused = False
        self.startTime = time.time()
        self.currentTime = time.time() - self.startTime + self.cancelTime
        return self.currentTime
