import cv2

# From the connected camera, in realtime, runs the calibration
# process using a chess board

class IncrementalCalibration:
    def __init__(self, calibration, numImages):
        self.numImages = numImages
        self.rms = 100000
        self.calibration = calibration
        self.corners = []
        self.K = None
        self.D = None
        self.rms = None
        print("Incremental calibration created")

    def process(self, frame):
        flipped = cv2.flip(frame, -1)  # upside-down and left-righ

        cv2.imshow("Calibration", flipped)
        cv2.waitKey(100)
        ret, corners = self.calibration.findChessboard(flipped)

        if ret:
            self.corners.append(corners)
            print(f'Captured {len(self.corners)} images of {self.numImages}')

            if len(self.corners) > self.numImages:
                K,D,rms = self.calibration.refine(self.corners)
                self.K = K
                self.D = D
                self.rms = rms
                return -1

        return 0

