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
    def __init__(self, cameraId):
        self.cap = cv2.VideoCapture(cameraId)


    def process(self, callback):
        while True:
            ret, frame = self.cap.read()
            if not ret: break

            # Press ESC to exit
            ret, bytesFrame = callback(frame)
            if ret == -1 or cv2.waitKey(1) & 0xFF == 27: break
            if not bytesFrame  == None: yield bytesFrame

        self.cap.release()
