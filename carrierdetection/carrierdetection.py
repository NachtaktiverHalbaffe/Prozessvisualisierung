"""
Filename: carrierdetection.py
Version name: 0.1, 2021-05-20
Short description: Module for detecting the carrier with ultrasonic sensor

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
import RPi.GPIO as GPIO
import time
import logging
from threading import Thread, Event
from api.constants import FILE_HANDLER_PV, STREAM_HANDLER


class CarrierDetection(object):

    def __init__(self):
        self.distanceEntrance = 0.0
        self.distanceExit = 0.0
        self.baseLevel = 0.0
        self.detectedIntrusion = False
        self.stopFlag = Event()
        self.stopFlag.clear()

        # setup sensors
        self.GPIO_TRIGGER_1 = 23  # entrance
        self.GPIO_TRIGGER_2 = 16  # exit
        self.GPIO_ECHO_1 = 24  # entrance
        self.GPIO_ECHO_2 = 18  # exit
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.GPIO_TRIGGER_1, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_1, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER_2, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_2, GPIO.IN)

        # setup logging
        self.logger = logging.getLogger("processvisualisation")
        self.logger.setLevel(logging.INFO)
        # add logger handler to logger
        self.logger.handlers = []
        self.logger.addHandler(STREAM_HANDLER)
        self.logger.addHandler(FILE_HANDLER_PV)

    def calibrate(self):
        time.sleep(0.5)
        self._measureExit()
        time.sleep(0.5)
        self._measureEntrance()
        if abs(self.distanceEntrance - self.distanceExit) < 6:
            GPIO.cleanup()
            self.baseLevel = (self.distanceEntrance+self.distanceExit)/2
            # format baselevel to 2 decimal places
            self.baseLevel = "{:.2f}".format(self.baseLevel)
            return
        else:
            GPIO.cleanup()
            self.baseLevel = 0.0
            return

    def detectCarrier(self, exspected, baseLevelHeight):
        isExpected = False
        self.distanceEntrance = 0.0
        self.distanceExit = 0.0

        while True:
            time.sleep(0.1)
            self._measureEntrance()
            time.sleep(0.1)
            self._measureExit()

            if exspected == 'entrance':
                if baseLevelHeight - self.distanceExit > 10:
                    self.logger.info(
                        "[CARRIERDETECTION] Detected carrier on exit")
                    isExpected = False
                    break
                if baseLevelHeight - self.distanceEntrance > 10:
                    self.logger.info(
                        "[CARRIERDETECTION] Detected carrier on entrance")
                    isExpected = True
                    break
            elif exspected == 'exit':
                if baseLevelHeight - self.distanceEntrance > 10:
                    self.logger.info(
                        "[CARRIERDETECTION] Detected carrier on entrance")
                    isExpected = False
                    break
                if baseLevelHeight - self.distanceExit > 10:
                    isExpected = True
                    self.logger.info(
                        "[CARRIERDETECTION] Detected carrier on exit")
                    break
            elif exspected == 'both':
                if baseLevelHeight - self.distanceEntrance > 10 or baseLevelHeight - self.distanceExit > 10:
                    isExpected = True
                    self.logger.info("[CARRIERDETECTION] Detected carrier")
                    break
        GPIO.cleanup()
        return isExpected

    def checkForIntrusion(self, baseLevelHeight):
        self.distanceEntrance = 0.0
        self.distanceExit = 0.0
        baseLevelHeight = float(baseLevelHeight)
        while not self.stopFlag.isSet():
            time.sleep(0.3)
            self._measureEntrance()
            time.sleep(0.3)
            self._measureExit()
            if baseLevelHeight - self.distanceExit > 10 or baseLevelHeight - self.distanceEntrance > 10:
                self.detectedIntrusion = True
            else:
                self.detectedIntrusion = False
        self.stopFlag.clear()

    def kill(self):
        self.stopFlag.set()

    def _measureEntrance(self):
        GPIO.output(self.GPIO_TRIGGER_1, True)
        time.sleep(0.00002)
        GPIO.output(self.GPIO_TRIGGER_1, False)
        while GPIO.input(self.GPIO_ECHO_1) == False:
            time_start = time.time()
        while GPIO.input(self.GPIO_ECHO_1) == True:
            time_end = time.time()
        # the measured distance is output in cm
        # distance = (delta_time * schallgeschw.)/ 2
        self.distanceEntrance = ((time_end - time_start) * 34300) / 2

    def _measureExit(self):
        GPIO.output(self.GPIO_TRIGGER_2, True)
        time.sleep(0.00002)
        GPIO.output(self.GPIO_TRIGGER_2, False)
        while GPIO.input(self.GPIO_ECHO_2) == False:
            time_start = time.time()
        while GPIO.input(self.GPIO_ECHO_2) == True:
            time_end = time.time()
        # the measured distance is output in cm
        # distance = (delta_time * schallgeschw.)/ 2
        self.distanceExit = ((time_end - time_start) * 34300) / 2
