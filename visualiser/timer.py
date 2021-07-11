"""
Filename: timer.py
Version name: 1.0, 2021-07-10
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

    # start timer
    def start(self):
        self.startTime = time.time()

    # pause timer
    def pause(self):
        self.isPaused = True
        self.currentTime = self.getTime()
        self.cancelTime = self.currentTime
        return self.currentTime

    # get current time of timer
    def getTime(self):
        if self.cancelTime == None:
            self.currentTime = time.time() - self.startTime
        else:
            self.currentTime = time.time() - self.startTime + self.cancelTime
        return self.currentTime

    # resume timer after timer got paused
    def resume(self):
        self.isPaused = False
        self.startTime = time.time()
        self.currentTime = time.time() - self.startTime + self.cancelTime
        return self.currentTime
