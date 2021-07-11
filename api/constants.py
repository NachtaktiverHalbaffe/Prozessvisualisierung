"""
Filename: constants.py
Version name: 1.0, 2021-07-10
Short description: system wide constants

(C) 2003-2021 IAS, Universitaet Stuttgart

"""

import os
import logging
from carrierdetection.carrierdetection import CarrierDetection

CWP_DIR = os.path.dirname(os.getcwd())
#IP_MES = "http://129.69.102.129"
#IP_MES = "http://127.0.0.1"
IP_MES = "http://192.168.178.30"
calibrater = CarrierDetection()
calibrater.calibrate()
BASE_LEVEL_HEIGHT = calibrater.baseLevel

# logging constants
LOG_FORMATTER = logging.Formatter('[%(asctime)s ] %(message)s')
FILE_HANDLER_PV = logging.FileHandler("processvisualisation.log")
FILE_HANDLER_PV.setFormatter(LOG_FORMATTER)
FILE_HANDLER_PV.setLevel(logging.INFO)
FILE_HANDLER_ERROR = logging.FileHandler("errors.log")
FILE_HANDLER_ERROR.setFormatter(LOG_FORMATTER)
FILE_HANDLER_ERROR.setLevel(logging.INFO)
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(LOG_FORMATTER)
STREAM_HANDLER.setLevel(logging.INFO)
