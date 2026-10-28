import cv2
import sys

video_path = sys.argv[1]

cap = cv2.VideoCapture(video_path)

# Choose frame number
frame_number = 100

cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

ret, frame = cap.read()

if ret:
    cv2.imwrite("frame.jpg", frame)
    print("Frame saved")
else:
    print("Could not read frame")

cap.release()
