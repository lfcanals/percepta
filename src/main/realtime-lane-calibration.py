from camera.camera import Camera
from calibration.eyeFishRectification import EyeFishRectification
from lanedetection.laneDetection import LaneDetector
from realtime.borderCalibration import RealtimeLaneCalibration
from realtime.calibrationFiles import *
import cv2
import sys
import json
import numpy as np


print("Usage:")
print("    " + sys.argv[0] + " cameraId left|right")
print()
print("Press ESC when the car is ON the line")

cameraId = int(sys.argv[1])
leftOrRight = sys.argv[2]


if leftOrRight == 'left':
    laneLimitsFile = 'lane-calibration-left.json'
elif leftOrRight == 'right':
    laneLimitsFile = 'lane-calibration-right.json'
else:
    print("Error in usage. 2nd parameter must be 'left' or 'right'")
    exit


with open(calibrationFile, "r") as f:
    data = json.load(f)
    K = np.array(data["K"])
    D = np.array(data["D"])



cam = Camera(cameraId)
realtimeLaneDetection = RealtimeLaneCalibration(EyeFishRectification(K, D), LaneDetector())
cam.process(realtimeLaneDetection.process)
cv2.destroyAllWindows()

print(realtimeLaneDetection.lanesLines)

writeLaneLimits(leftOrRight, realtimeLaneDetection)
