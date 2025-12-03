import cv2

class RealtimeLaneCalibration:
    def __init__(self, rectifier, laneDetector):
        self.rectifier = rectifier
        self.laneDetector = laneDetector

    def process(self, frame):
        print("Images are NOT flip!!! Change the code to flip it")
        flipped = frame #cv2.flip(frame, -1)  # upside-down and left-righ

        recImg = self.rectifier.rectify(flipped)
        laneImgs, self.lanesLines = self.laneDetector.calculateLines(recImg)

        cv2.imshow("Lanes", laneImgs);
        return 0

