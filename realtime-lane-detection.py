from camera.camera import Camera
from calibration.eyeFishRectification import EyeFishRectification
from lanedetection.laneDetection import LaneDetector
from runtime.laneDetection import RealtimeLaneDetection
from runtime.calibrationFiles import *
import cv2
import sys
import json


print("Usage:")
print("    " + sys.argv[0] + " cameraId [debug]")

cameraId = int(sys.argv[1])
if len(sys.argv) > 2 and sys.argv[2] == 'debug': 
    debug = True
else: 
    debug = False

K,D = readEyeFishCalibration()
leftLine, rightLine = readLaneLimits()

cam = Camera(cameraId)
realtimeLaneDetection = RealtimeLaneDetection(EyeFishRectification(K, D), \
        LaneDetector(debug), leftLine, rightLine)
cam.process(realtimeLaneDetection.process)
cv2.destroyAllWindows()
