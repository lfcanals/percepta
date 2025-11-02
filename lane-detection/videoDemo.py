import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from laneDetection import LaneDetector

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import VideoClip


laneLines = LaneDetector()
clip1 = VideoFileClip("video_input.mp4")


def make_frame(t):
    frame = clip1.get_frame(t)
    return laneLines.calculateLines(frame)[0]

# Create a new video clip with the same duration and FPS
transformed_clip = VideoClip(make_frame, duration=clip1.duration)
transformed_clip.fps = clip1.fps

#white_clip = clip1.fl_image(laneLines.calculateLines)
transformed_clip.write_videofile('video_output.mp4', audio=False)

clip1.close()
transformed_clip.close()
