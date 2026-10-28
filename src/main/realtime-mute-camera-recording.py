from camera.camera import Camera
from recording.recorder import Recorder
import cv2
import sys


print("Usage:")
print("    " + sys.argv[0] + " cameraId folder")

cameraId = int(sys.argv[1])
folder = sys.argv[2]
maxSize = 40960000 # 40 Mb

cam = Camera(cameraId)
recorder = Recorder(maxSize, folder)

cam.process(recorder.process)
