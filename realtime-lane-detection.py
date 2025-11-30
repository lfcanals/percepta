from camera.camera import Camera
from calibration.eyeFishRectification import EyeFishRectification
from lanedetection.laneDetection import LaneDetector
import cv2
import sys
import json
import numpy as np




class RealtimeLaneDetection:
    def __init__(self, K, D, leftLine, rightLine):
        self.rectifier = EyeFishRectification(K, D)
        self.laneDetector = LaneDetector()
        self.startPointLineLeft = (round(leftLine[0]), round(leftLine[1]))
        self.endPointLineLeft = (round(leftLine[2]), round(leftLine[3]))

        self.startPointLineRight = (round(rightLine[0]), round(rightLine[1]))
        self.endPointLineRight = (round(rightLine[2]), round(rightLine[3]))
        self.colorGuidelines = (255, 255, 255) # White

        print("Images are NOT flip!!! Change the code to flip it")
        
    def process(self, frame):
        flipped = frame #cv2.flip(frame, -1)  # upside-down and left-righ

        recImg = self.rectifier.rectify(flipped)
        laneImgs, lanesLines = self.laneDetector.calculateLines(recImg)

        cv2.line(laneImgs,self.startPointLineLeft,self.endPointLineLeft,self.colorGuidelines,3)
        cv2.line(laneImgs,self.startPointLineRight,self.endPointLineRight,self.colorGuidelines,3)

        cv2.imshow("Lanes", laneImgs);
        return 0




cameraId = int(sys.argv[1])
calibrationFile = 'calibration-camera.json'
leftLineFile = 'lane-calibration-left.json'
rightLineFile = 'lane-calibration-right.json'

with open(calibrationFile, "r") as f:
    data = json.load(f)
    K = np.array(data["K"])
    D = np.array(data["D"])

with open(leftLineFile, "r") as f:
    data = json.load(f)
    leftLine = data['leftLine']

with open(rightLineFile, "r") as f:
    data = json.load(f)
    rightLine = data['rightLine']




cam = Camera(cameraId)
realtimeLaneDetection = RealtimeLaneDetection(K, D, leftLine, rightLine)
cam.process(realtimeLaneDetection.process)
cv2.destroyAllWindows()
