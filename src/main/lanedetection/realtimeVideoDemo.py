import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from laneDetection import LaneDetector

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import VideoClip

import time
import cv2


laneLines = LaneDetector()
clip1 = cv2.VideoCapture(str(sys.argv[1]))


# Get the frame rate for real-time playback
fps = clip1.get(cv2.CAP_PROP_FPS)
delay = 1 / (2*fps) if fps > 0 else 1 / 60  # Fallback to 30 FPS if unknown

while True:
    ret, frame = clip1.read()
    if not ret:
        break  # End of video

    # Apply your custom transformation
    transformed_frame = laneLines.calculateLines(frame)[0]

    # Display the transformed frame
    cv2.imshow("Transformed Video", transformed_frame)

    # Real-time playback control (press 'q' to quit)
    if cv2.waitKey(int(delay * 1000)) & 0xFF == ord('q'):
        break

clip1.release()
cv2.destroyAllWindows()
