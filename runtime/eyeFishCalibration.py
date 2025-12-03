import cv2

# From the connected camera, in realtime, runs the calibration
# process using a chess board

class IncrementalCalibration:
    def __init__(self, calibration):
        self.rms = 100000
        self.calibration = calibration
        self.corners = []
        self.K = None
        self.D = None
        self.rms = None

    def process(self, frame):
        flipped = cv2.flip(frame, -1)  # upside-down and left-righ

        ret, corners = self.calibration.findChessboard(flipped)

        if ret:
            cv2.imshow("Chessboard", flipped)
            self.corners.append(corners)

            if len(self.corners) > numImages:
                K,D,rms = self.calibration.refine(self.corners)
                self.K = K
                self.D = D
                self.rms = rms
                return -1

        cv2.imshow("Flipped Webcam", flipped)
        return 0

