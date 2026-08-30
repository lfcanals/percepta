from moviepy.editor import *
import sys

fileIn = sys.argv[1]
f = sys.argv[2]
t = sys.argv[3]
fileOut = sys.argv[4]
clip = VideoFileClip(fileIn).subclip(f, t)

clip.write_videofile(fileOut, codec="libx264", audio_codec="aac")
