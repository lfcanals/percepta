from camera.camera import Camera
from calibration.eyeFishCalibration import EyeFishCalibration
from runtime.eyeFishCalibration import IncrementalCalibration
from runtime.calibrationFiles import *
import cv2
import sys
import json


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
