
# Dependencies
    * Python 
    * OpenCV: `pip install opencv-python` (ETA: 60 minutes)
    * MoviePy: 'pip install moviepy`

# Fast guide : how to demo
There are three demo python files:
    * onePhotoDemo.py : which receives a photo and decorates with the lane lines
    * videoDemo.py : which receives a video and records a decorated video as 'video_ouput.mp4'
    * realtimeVideoDemo.py : which decorates in realtime a video

The rest of Python files are:
    * laneDetection.py : contains the object for lane detection for a frame


The most espectacular is to decorate a video.
There is demo video under 'test' folder: france1.mp4 which is a French highway.
To see in realtime working, just type:

    python realtimeVideoDemo.py test/france1.mp4

# Next features:
    1. Inertial lane lines: DONE!
    2. Rectification of eye-fish view: see other folder "calibration"
    3. Callibration: position of the car between the lines; limits
    2. Detection of turns
    3. Extra: top view
    4. Distance marks in lanes
    5. Centered position of the car to the left and right lane


# TODO
Write an article explaining all the maths behind. Just the maths, not the visual explanations.

# Ideas
Reuse the previous calculations for next image.

Do the different stages of the conversion in parallel to provide faster answers

At the end of [this article] (https://github.com/NurNils/opencv-lane-detection) 
there is a "car detection" included.

Use the "Area of Interest" to:
    1. Separate the view in "urgent things": area of interest
    2. "Important things": moving from out-of-the area of interest into it

