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
        self.DETECT_THRESHOLD = 3
        self.INTRUSION_THRESHOLD = 5
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
        self.stopFlag.clear()
        self._measureExit(sample_size=11)
        time.sleep(0.5)
        self._measureEntrance(sample_size=11)
        print("[CALIBRATE] Distance on enrtance: " + str(self.distanceEntrance))
        print("[CALIBRATE] Distance on exit: " + str(self.distanceExit))

        if abs(self.distanceEntrance - self.distanceExit) < 20:
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
        self.stopFlag.clear()
        self.detectedOnEntrance = False
        self.detectedOnExit = False
        self.distanceEntrance = baseLevelHeight
        self.distanceExit = baseLevelHeight

        while not self.stopFlag.isSet():
            try:
                self._measureEntrance(sample_size=3)
                self._measureExit(sample_size=3)
            except Exception as e:
                self.logger.error('[CARRIERDETECTION] Scan currently not possible. Exception: ', e)
                self.distanceEntrance = baseLevelHeight
                self.distanceExit = baseLevelHeight
            
    
            #check for detection on exit
            if baseLevelHeight - self.distanceExit > self.DETECT_THRESHOLD:
                self.detectedOnExit = True
                self.stopFlag.clear()
                self.logger.info("[CARRIERDETECTION] Detected Carrier on Exit")
            else:
                self.detectedOnExit = False
            #check for detection on entrance
            if baseLevelHeight - self.distanceEntrance > self.DETECT_THRESHOLD:
                self.detectedOnEntrance = True
                self.stopFlag.clear()
                self.logger.info("[CARRIERDETECTION] Detected Carrier on Entrance")
            else:
                self.detectedOnEntrance = False
                self.stopFlag.clear()

            
        
    # measures if a intrusion is detected on either the entrance or exit. 
    # Doesnt care where its detected, only checks for general intrusion
    def checkForIntrusion(self, baseLevelHeight):
        self.stopFlag.clear()
        baseLevelHeight = float(baseLevelHeight)
        "{:.2f}".format(baseLevelHeight)
        while not self.stopFlag.isSet():
            if baseLevelHeight - self.distanceExit > self.INTRUSION_THRESHOLD or baseLevelHeight - self.distanceEntrance > self.INTRUSION_THRESHOLD:
                self.detectedIntrusion = True
            else:
                self.detectedIntrusion = False
        self.stopFlag.clear()

    # stop the carrierdetection threads
    def kill(self):
        #GPIO.cleanup()
        self.stopFlag.set()

    # sensor logic on the sensor on the entrance
    def _measureEntrance(self, sample_size = 7, sample_wait = 0.1):
        samples = []
        for sample in range(sample_size):
            time_end= 0
            time_start=0
            GPIO.output(self.GPIO_TRIGGER_1, GPIO.LOW)
            time.sleep(sample_wait)
            GPIO.output(self.GPIO_TRIGGER_1, True)
            time.sleep(0.00002)
            GPIO.output(self.GPIO_TRIGGER_1, False)
            echo_status_counter = 1
            while GPIO.input(self.GPIO_ECHO_1) == False:
                    if echo_status_counter < 10000:
                        time_start = time.time()
                        echo_status_counter += 1
                    else:
                        return       
            while GPIO.input(self.GPIO_ECHO_1) == True:
                time_end = time.time()
            # the measured distance is output in cm
            # distance = (delta_time * schallgeschw.)/ 2
            if (time_start != 0 and time_end !=0):
                samples.append(((time_end - time_start) * 34300) / 2)
        # calculating with avergae value
        #self.distanceEntrance = sum(samples)/len(samples)
        # calculating with median
        self.distanceEntrance = sorted(samples)[len(samples) //2]


    # sensor logic on the sensor on the exit
    def _measureExit(self,sample_size = 7, sample_wait = 0.1):
        samples = []
        for sample in range(sample_size):
            time_end= 0
            time_start=0
            GPIO.output(self.GPIO_TRIGGER_2, GPIO.LOW)
            time.sleep(sample_wait)
            GPIO.output(self.GPIO_TRIGGER_2, True)
            time.sleep(0.00002)
            GPIO.output(self.GPIO_TRIGGER_2, False)
            echo_status_counter = 1
            while GPIO.input(self.GPIO_ECHO_2) == False:
                if echo_status_counter < 10000:
                        time_start = time.time()
                        echo_status_counter += 1
                else:
                    return   
            while GPIO.input(self.GPIO_ECHO_2) == True:
                time_end = time.time()
            # the measured distance is output in cm
            # distance = (delta_time * schallgeschw.)/ 2
            if (time_start != 0 and time_end !=0):
                samples.append(((time_end - time_start) * 34300) / 2)
        # calculating with avergae value
        #self.distanceExit = sum(samples)/len(samples)
        # calculating with median
        self.distanceExit = sorted(samples)[len(samples) //2]
