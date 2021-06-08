"""
Filename: carrierdetection.py
Version name: 0.1, 2021-05-20
Short description: Module for detecting the carrier with ultrasonic sensor

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
import RPi.GPIO as GPIO
import time


class CarrierDetection(object):

    def __init__(self):
        self.GPIO_TRIGGER_1 = 23  # GPIO23
        self.GPIO_TRIGGER_2 = 16  # GPIO4
        self.GPIO_ECHO_1 = 24  # GPIO24
        self.GPIO_ECHO_2 = 18  # GPIO4
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.GPIO_TRIGGER_1, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_1, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER_2, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_2, GPIO.IN)

    def calibrate(self):
        #distanceEntrance = self._measureEntrance()
        #distanceExit = self._measureExit()
        distanceEntrance= 0
        distanceExit= 0
        if abs(distanceEntrance - distanceExit) < 2:
            return (distanceEntrance+distanceExit)/2
        else:
            return 0

    def detectCarrier(self, exspected, baseLevelHeight):
        isExpected = False

        while True:
            distanceEntrance = self._measureEntrance()
            time.sleep(0.2)
            distanceExit = self._measureExit()
            time.sleep(0.2)

            if exspected == 'entrance':
                if baseLevelHeight - distanceExit > 10:
                    isExpected = False
                    break
                if baseLevelHeight - distanceEntrance > 10:
                    isExpected = True
                    break
            elif exspected == 'exit':
                if baseLevelHeight - distanceEntrance > 10:
                    isExpected = False
                    break
                if baseLevelHeight - distanceExit > 10:
                    isExpected = True
                    break
            elif exspected == 'both':
                if baseLevelHeight - distanceEntrance > 10 or baseLevelHeight - distanceExit > 10:
                    isExpected = True
                    break

        GPIO.cleanup()
        return isExpected

    def _measureEntrance(self):
        GPIO.output(self.GPIO_TRIGGER_1, True)
        time.sleep(0.00002)
        GPIO.output(self.GPIO_TRIGGER_1, False)
        time_start = time.time()
        time_end = time.time()
        while GPIO.input(self.GPIO_ECHO_1) == False:
            time_start = time.time()
        while GPIO.input(self.GPIO_ECHO_1) == True:
            time_end = time.time()
        # the measured distance is output in cm
        # distance = (delta_time * schallgeschw.)/ 2
        return ((time_end - time_start) * 34300) / 2


    def _measureExit(self):
        GPIO.output(self.GPIO_TRIGGER_2, True)
        time.sleep(0.00002)
        GPIO.output(self.GPIO_TRIGGER_2, False)
        time_start = time.time()
        time_end = time.time()
        while GPIO.input(self.GPIO_ECHO_2) == False:
            time_start = time.time()
        while GPIO.input(self.GPIO_ECHO_2) == True:
                time_end = time.time()
        # the measured distance is output in cm
        # distance = (delta_time * schallgeschw.)/ 2
        return ((time_end - time_start) * 34300) / 2

