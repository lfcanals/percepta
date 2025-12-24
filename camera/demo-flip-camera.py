import cv2
import sys
from camera import Camera


def flipAndShow(frame):
    flipped = cv2.flip(frame, -1)  # upside-down and left-righ
    cv2.imshow("Flipped Webcam", flipped)



cam = Camera(int(sys.argv[1]))
cam.process(flipAndShow)
cv2.destroyAllWindows()
