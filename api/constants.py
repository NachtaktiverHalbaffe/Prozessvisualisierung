import os
from carrierdetection.carrierdetection import CarrierDetection

CWP_DIR = os.path.dirname(os.getcwd())
#IP_MES = "http://129.69.102.129"
#IP_MES = "http://127.0.0.1"
IP_MES = "http://192.168.178.30"
calibrater = CarrierDetection()
calibrater.calibrate()
BASE_LEVEL_HEIGHT = calibrater.baseLevel
