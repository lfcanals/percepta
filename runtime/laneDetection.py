# From the camera, in realtime, shows lane lines
# and reports when the right or left lanes are too close
import cv2

class RealtimeLaneDetection:
    def __init__(self, rectifier, laneDetector, leftLine, rightLine):
        self.rectifier = rectifier
        self.laneDetector = laneDetector
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


