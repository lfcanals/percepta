from camera.camera import Camera
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

cam = Camera(cameraId)
incrementalCalibration = IncrementalCalibration(EyeFishCalibration(7,7))
cam.process(incrementalCalibration.process)
cv2.destroyAllWindows()

print(f"K={incrementalCalibration.K}");
print(f"D={incrementalCalibration.D}");
print(f"error={incrementalCalibration.rms}");

writeEyeFishCalibration(incrementalCalibration)
