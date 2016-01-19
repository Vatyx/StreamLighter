import urllib2
import time
import livestreamer

streams = livestreamer.streams("http://www.twitch.tv/starladder1")
stream = streams["source"]
fd=stream.open()

data=fd.read(2048000)
fd.close()
filename = "test.dat"

f= open(filename, 'wb')
f.write(data)
f.close()



# print "Recording video..."
# response = urllib2.urlopen("http://www.twitch.tv/starladder1")
# filename = time.strftime("%Y%m%d%H%M%S",time.localtime())+".avi"
# f = open(filename, 'wb')

# video_file_size_start = 0  
# video_file_size_end = 1048576 * 7  # end in 7 mb 
# block_size = 1024

# start_time_in_seconds = time.time()
# time_limit = 10
# while 1:
#     try:
#         buffer = response.read(block_size)
#         if not buffer:
#             break
#         video_file_size_start += len(buffer)
#         if video_file_size_start > video_file_size_end:
#             break
#         f.write(buffer)

#     except Exception, e:
#         print(e)
# f.close()