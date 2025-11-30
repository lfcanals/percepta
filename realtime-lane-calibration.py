from camera.camera import Camera
from calibration.eyeFishRectification import EyeFishRectification
from lanedetection.laneDetection import LaneDetector
import cv2
import sys
import json
import numpy as np



cameraId = int(sys.argv[1])
leftOrRight = sys.argv[2]
calibrationFile = 'calibration-camera.json'



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


class RealtimeLaneCalibration:
    def __init__(self, K, D):
        self.rectifier = EyeFishRectification(K, D)
        self.laneDetector = LaneDetector()
        
    def process(self, frame):
        print("Images are NOT flip!!! Change the code to flip it")
        flipped = frame #cv2.flip(frame, -1)  # upside-down and left-righ

        recImg = self.rectifier.rectify(flipped)
        laneImgs, self.lanesLines = self.laneDetector.calculateLines(recImg)

        cv2.imshow("Lanes", laneImgs);
        return 0



cam = Camera(cameraId)
realtimeLaneDetection = RealtimeLaneCalibration(K, D)
cam.process(realtimeLaneDetection.process)
cv2.destroyAllWindows()

print(realtimeLaneDetection.lanesLines)

with open(laneLimitsFile, "w") as f:
    data = {}
    if leftOrRight == 'left':
        data['leftLine'] = realtimeLaneDetection.lanesLines[0];
    else:
        data['rightLine'] = realtimeLaneDetection.lanesLines[1];

    json.dump(data, f, indent=4)
