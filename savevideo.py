from moviepy.editor import *

clip = VideoFileClip("testvideo.dat").subclip(0,7)

clip = clip.volumex(0.8)

#clip.write_videofile("hopethisworks.webm")
