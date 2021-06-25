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
from hcsr04sensor import sensor


class CarrierDetection(object):

    def __init__(self):
        self.DETECT_THRESHOLD = 100
        self.distanceEntrance = 0.0
        self.distanceExit = 0.0
        self.baseLevel = 0.0
        self.detectedOnEntrance = False
        self.detectedOnExit = False
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
        self.sensorEntrance = sensor.Measurement(self.GPIO_TRIGGER_1, self.GPIO_ECHO_1)
        self.sensorExit = sensor.Measurement(self.GPIO_TRIGGER_2,self.GPIO_ECHO_2)

        # setup logging
        self.logger = logging.getLogger("processvisualisation")
        self.logger.setLevel(logging.INFO)
        # logging format
        log_formatter = logging.Formatter('[%(asctime)s ] %(message)s')
        file_handler_pv = logging.FileHandler("processvisualisation.log")
        file_handler_pv.setFormatter(log_formatter)
        file_handler_pv.setLevel(logging.INFO)
        file_handler_error = logging.FileHandler("errors.log")
        file_handler_error.setFormatter(log_formatter)
        file_handler_error.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        stream_handler.setLevel(logging.INFO)
        # add logger handler to logger
        self.logger.handlers = []
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler_pv)


    # measure the baselevelheight
    def calibrate(self):
        self.distanceEntrance = self.sensorEntrance.raw_distance()
        time.sleep(0.5)
        self.distanceExit = self.sensorExit.raw_distance()
        if abs(self.distanceEntrance - self.distanceExit) < 6:
            self.baseLevel = (self.distanceEntrance+self.distanceExit)/2
            # format baselevel to 2 decimal places
            self.baseLevel = "{:.2f}".format(self.baseLevel)
            self.kill()
            return
        else:
            self.baseLevel = 0.0
            self.kill()
            return

    # detect the carrier on either entrance or exit if the unit. 
    # Runs in a thread in processvisualisation
    def detectCarrier(self, baseLevelHeight):
        self.stopFlag.clear()
        self.detectedOnEntrance = False
        self.detectedOnExit = False
        self.distanceEntrance = 0.0
        self.distanceExit = 0.0
        self.distanceEntrance = 0.0
        self.distanceExit = 0.0

        while not self.stopFlag.isSet():
            try:
                self.distanceEntrance = self.sensorEntrance.raw_distance()
                time.sleep(0.5)
                self.distanceExit = self.sensorExit.raw_distance()

                #check for detection on exit
                if baseLevelHeight - self.distanceExit > self.DETECT_THRESHOLD:
                    self.detectedOnExit = True
                    self.stopFlag.clear()
                else:
                    self.detectedOnExit = False
                #check for detection on entrance
                if baseLevelHeight - self.distanceEntrance > self.DETECT_THRESHOLD:
                    self.detectedOnEntrance = True
                    self.stopFlag.clear()
                else:
                    self.detectedOnEntrance = False
                    self.stopFlag.clear()

            except Exception as e:
                self.logger.error('[CARRIERDETECTION] Scan currently not possible. Exception: ', e)
                self.kill()
        
    # measures if a intrusion is detected on either the entrance or exit. 
    # Doesnt care where its detected, only checks for general intrusion
    def checkForIntrusion(self,baseLevelHeight):
        self.stopFlag.clear()
        baseLevelHeight = float(baseLevelHeight)
        "{:.2f}".format(baseLevelHeight)
        while not self.stopFlag.isSet():
            time.sleep(0.3)
            self._measureEntrance()
            time.sleep(0.3)
            self._measureExit()
            if baseLevelHeight - self.distanceExit > self.DETECT_THRESHOLD or baseLevelHeight - self.distanceEntrance > self.DETECT_THRESHOLD:
                self.detectedIntrusion = True
            else:
                self.detectedIntrusion = False
        self.stopFlag.clear()

    # stop the carrierdetection threads
    def kill(self):
        #GPIO.cleanup()
        self.stopFlag.set()

    # sensor logic on the sensor on the entrance
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

        time.sleep(0.5)

    # sensor logic on the sensor on the exit
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

        time.sleep(0.5)
