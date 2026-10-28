from camera import Camera
from calibration.eyeFishCalibration import EyeFishCalibration
from realtime.eyeFishCalibration import IncrementalCalibration
from realtime.calibrationFiles import *
import cv2
import sys
import json


print("Usage:")
print("    " + sys.argv[0] + " cameraId numImages")
print()
cameraId = int(sys.argv[1])
numImages = int(sys.argv[2])

cam = Camera(cameraId, -1)
# 7x7 normal chess board

incrementalCalibration = IncrementalCalibration(EyeFishCalibration(7,7), numImages)
for result in cam.process(incrementalCalibration.process): 
    if incrementalCalibration.K is not None: break



cv2.destroyAllWindows()

print(f"K={incrementalCalibration.K}");
print(f"D={incrementalCalibration.D}");
print(f"error={incrementalCalibration.rms}");

writeEyeFishCalibration(incrementalCalibration)
