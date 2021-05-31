"""
Filename: carrierdetection.py
Version name: 0.1, 2021-05-20
Short description: Module for detecting the carrier with ultrasonic sensor

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
#import Rpi.GPIO as GPIO
import time


class CarrierDetection(object):

    def __init__(self):
        self.GPIO_TRIGGER_1 = 23  # GPIO23
        self.GPIO_TRIGGER_2 = 4  # GPIO4
        self.GPIO_ECHO_1 = 24  # GPIO24
        self.GPIO_ECHO_2 = 17  # GPIO4
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setwarnings(False)
        # GPIO.setup(self.GPIO_TRIGGER_1, GPIO.OUT)
        # GPIO.setup(self.GPIO_ECHO_1, GPIO.IN)
        # GPIO.setup(self.GPIO_TRIGGER_2, GPIO.OUT)
        # GPIO.setup(self.GPIO_ECHO_2, GPIO.IN)

    def calibrate(self):
        distanceEntrance = self._measureEntrance()
        distanceExit = self._measureExit()
        if abs(distanceEntrance - distanceExit) < 2:
            return (distanceEntrance+distanceExit)/2
        else:
            return 0

    def detectCarrier(self, expected, baseLevelHeight):
        isExpected = False

        while True:
            distanceEntrance = self._measureEntrance()
            time.sleep(0.5)
            distanceExit = self._measureExit()
            time.sleep(0.5)

            if expected == 'entrance':
                if baseLevelHeight - distanceExit > 4:
                    isExpected = False
                    break
                if baseLevelHeight - distanceEntrance > 4:
                    isExpected = True
                    break
            elif expected == 'exit':
                if baseLevelHeight - distanceEntrance > 4:
                    isExpected = False
                    break
                if baseLevelHeight - distanceExit > 4:
                    isExpected = True
                    break
        return isExpected

    def _measureEntrance(self):
        try:
            #GPIO.output(self.GPIO_TRIGGER_1, True)
            time.sleep(0.00002)
            #GPIO.output(self.GPIO_TRIGGER_1, False)
            time_start = time.time()
            time_end = time.time()
            # while GPIO.input(self.GPIO_ECHO_1) == 0:
            #     time_start = time.time()
            # while GPIO.input(self.GPIO_ECHO_1) == 1:
            #     time_end = time.time()
            # the measured distance is output in cm
            # distance = (delta_time * schallgeschw.)/ 2
            return ((time_end - time_start) * 34300) / 2

        except Exception as e:
            pass

    def _measureExit(self):
        try:
            #GPIO.output(self.GPIO_TRIGGER_2, True)
            time.sleep(0.00002)
            #GPIO.output(self.GPIO_TRIGGER_2, False)
            time_start = time.time()
            time_end = time.time()
            # while GPIO.input(self.GPIO_ECHO_2) == 0:
            #     time_start = time.time()
            # while GPIO.input(self.GPIO_ECHO_2) == 1:
            #     time_end = time.time()
            # the measured distance is output in cm
            # distance = (delta_time * schallgeschw.)/ 2
            return ((time_end - time_start) * 34300) / 2

        except Exception as e:
            pass
