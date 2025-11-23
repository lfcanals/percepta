from camera.camera import Camera
from calibration.eyeFishRectification import EyeFishRectification
from lanedetection.laneDetection import LaneDetector
import cv2
import sys
import json
import numpy as np



cameraId = int(sys.argv[1])
calibrationFile = sys.argv[2]

with open(calibrationFile, "r") as f:
    data = json.load(f)

K = np.array(data["K"])
D = np.array(data["D"])


class RealtimeLaneDetection:
    def __init__(self, K, D):
        self.rectifier = EyeFishRectification(K, D)
        self.laneDetector = LaneDetector()
        
    def process(self, frame):
        flipped = cv2.flip(frame, -1)  # upside-down and left-righ

        recImg = self.rectifier.rectify(flipped)
        laneImgs, lanesLines = self.laneDetector.calculateLines(recImg)

        cv2.imshow("Lanes", laneImgs);
        return 0



cam = Camera(cameraId)
realtimeLaneDetection = RealtimeLaneDetection(K, D)
cam.process(realtimeLaneDetection.process)
cv2.destroyAllWindows()
