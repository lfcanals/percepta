import cv2

class Camera:
    def __init__(self, cameraId):
        self.cap = cv2.VideoCapture(cameraId)


    def process(self, callback):
        while True:
            ret, frame = self.cap.read()
            if not ret: break

            # Press ESC to exit
            if callback(frame) == -1 or cv2.waitKey(1) & 0xFF == 27: break

        self.cap.release()
