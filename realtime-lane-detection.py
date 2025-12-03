from camera.camera import Camera
from calibration.eyeFishRectification import EyeFishRectification
from lanedetection.laneDetection import LaneDetector
from runtime.laneDetection import RealtimeLaneDetection
import cv2
import sys
import json
import numpy as np





cameraId = int(sys.argv[1])

K,D = readEyeFishCalibration()
leftLine, rightLine = readLaneLimits()

cam = Camera(cameraId)
realtimeLaneDetection = RealtimeLaneDetection(EyeFishRectification(K, D), \
        LaneDetector(), leftLine, rightLine)
cam.process(realtimeLaneDetection.process)
cv2.destroyAllWindows()
