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
        GPIO.setup(self.GPIO_TRIGGER_1, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_1, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER_2, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_2, GPIO.IN)

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
        time.sleep(0.5)
        self._measureExit()
        time.sleep(0.5)
        self._measureEntrance()
        print(self.distanceExit)
        print(self.distanceEntrance)
        if abs(self.distanceEntrance - self.distanceExit) < 6:
            self.baseLevel = (self.distanceEntrance+self.distanceExit)/2
            # format baselevel to 2 decimal places
            self.baseLevel = "{:.2f}".format(self.baseLevel)
            return
        else:
            self.baseLevel = 0.0
            return

    # detect the carrier on either entrance or exit if the unit. 
    # Runs in a thread in processvisualisation
    def detectCarrier(self, baseLevelHeight):
        print(baseLevelHeight)
        self.stopFlag.clear()
        self.detectedOnEntrance = False
        self.detectedOnExit = False
        self.distanceEntrance = baseLevelHeight
        self.distanceExit = baseLevelHeight

        while not self.stopFlag.isSet():
            try:
                time.sleep(0.3)
                self._measureEntrance()
                time.sleep(0.3)
                self._measureExit()
            except Exception as e:
                self.logger.error('[CARRIERDETECTION] Scan currently not possible. Exception: ', e)
                self.distanceEntrance = baseLevelHeight
                self.distanceExit = baseLevelHeight

            #check for detection on exit
            if baseLevelHeight - self.distanceExit > self.DETECT_THRESHOLD:
                self.detectedOnExit = True
                self.stopFlag.clear()
                self.logger.info("[CARRIERDETECTION] Detected Carrier on Entrance")
            else:
                self.detectedOnExit = False
            #check for detection on entrance
            if baseLevelHeight - self.distanceEntrance > self.DETECT_THRESHOLD:
                self.detectedOnEntrance = True
                self.stopFlag.clear()
                self.logger.info("[CARRIERDETECTION] Detected Carrier on Exit")
            else:
                self.detectedOnEntrance = False
                self.stopFlag.clear()

            
        
    # measures if a intrusion is detected on either the entrance or exit. 
    # Doesnt care where its detected, only checks for general intrusion
    def checkForIntrusion(self, baseLevelHeight):
        self.stopFlag.clear()
        self.distanceEntrance = 0.0
        self.distanceExit = 0.0
        baseLevelHeight = float(baseLevelHeight)
        "{:.2f}".format(baseLevelHeight)
        while not self.stopFlag.isSet():
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
        echo_status_counter = 1
        while GPIO.input(self.GPIO_ECHO_1) == False:
                if echo_status_counter < 1000:
                    time_start = time.time()
                    echo_status_counter += 1
                else:
                    break       
        while GPIO.input(self.GPIO_ECHO_1) == True:
            time_end = time.time()
        # the measured distance is output in cm
        # distance = (delta_time * schallgeschw.)/ 2
        self.distanceEntrance = ((time_end - time_start) * 34300) / 2
        time.sleep(0.2)

    # sensor logic on the sensor on the exit
    def _measureExit(self):
        GPIO.output(self.GPIO_TRIGGER_2, True)
        time.sleep(0.00002)
        GPIO.output(self.GPIO_TRIGGER_2, False)
        echo_status_counter = 1
        while GPIO.input(self.GPIO_ECHO_2) == False:
            if echo_status_counter < 1000:
                    time_start = time.time()
                    echo_status_counter += 1
            else:
                break   
        while GPIO.input(self.GPIO_ECHO_2) == True:
            time_end = time.time()
        # the measured distance is output in cm
        # distance = (delta_time * schallgeschw.)/ 2
        self.distanceExit = ((time_end - time_start) * 34300) / 2
        time.sleep(0.2)
