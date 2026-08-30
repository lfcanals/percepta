import cv2

class Camera:
    """
         Camera object to be used to process images.

         Usage example:

            def callback(frame):
               # Do something with the frame 

            cam = Camera(0)
            cam.process(callback)
    """
    def __init__(self, cameraId, flip = 0):
        self.cap = cv2.VideoCapture(cameraId)
        self.flip = flip


    def process(self, callback):
        while True:
            ret, frame = self.cap.read()
            if not ret: break

            frame = cv2.flip(frame, self.flip)
            print(1)
            callback(frame)

            # Press ESC to exit
            if cv2.waitKey(1) & 0xFF == 27: break
            yield frame

        self.cap.release()
