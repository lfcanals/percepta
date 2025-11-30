from camera.camera import Camera
from calibration.eyeFishCalibration import EyeFishCalibration
import cv2
import sys
import json


cameraId = int(sys.argv[1])
numImages = int(sys.argv[2])
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





cam = Camera(cameraId)
incrementalCalibration = IncrementalCalibration(EyeFishCalibration(7,7))
cam.process(incrementalCalibration.process)
cv2.destroyAllWindows()

print(f"K={incrementalCalibration.K}");
print(f"D={incrementalCalibration.D}");
print(f"error={incrementalCalibration.rms}");

data={}
data['K']=incrementalCalibration.K
data['D']=incrementalCalibration.D
with open("calibration-camera.json", "w") as f:
    json.dump(data, f, indent=4)

