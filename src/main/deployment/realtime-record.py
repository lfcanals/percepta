import cv2
import sys


cap = cv2.VideoCapture(int(sys.argv[1]))
outFile = sys.argv[2]
ret, frame = cap.read()
height, width = frame.shape[:2]

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'avc1')
out = cv2.VideoWriter(outFile, fourcc, 20.0, (width, height))

if not out.isOpened():
    print("ERROR: VideoWriter failed to open")
    exit(1)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        out.write(frame)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
