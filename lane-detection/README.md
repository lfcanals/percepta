
# Dependencies
    * Python 
    * OpenCV: `pip install opencv-python` (ETA: 60 minutes)
    * MoviePy: 'pip install moviepy`


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

