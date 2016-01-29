import threading
import time
import sys
from livestreamer import Livestreamer
import subprocess
import socket
import string
from datetime import datetime

print("hi")

channel = "pianoimproman"


 
EIGHT_SECONDS = 4500000
FIVE_SECONDS = 3700000
DELAY = 13000000
 
threads = []

start = 0
end = 0

def create_highlight(start, end):
    import time
 
    print("CREATING HIGHLIGHT")

    subprocess.call(['ffmpeg', '-i', 'stream.dat', '-ss', str(start), '-t', str(end), '-async', '1', "hopethisworks1.mp4"])

    print("DONE!")

    # stream = open("stream.dat", 'rb')
    # stream.seek(start)
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    # highlight = open("highlight-" + timestr + ".dat", 'wb')
    # buffer = stream.read(end - start)
    # print(len(buffer))

    # highlight.write(buffer)

    # stream.close()
    # highlight.close()

    # print "highlight-" + timestr + ".dat"
 
def stream_recording():
 
    print("STARTING TO RECORD STREAM")

    session = Livestreamer()
    stream = session.streams('http://www.twitch.tv/' + channel)

    print("CONNECTED TO STREAM")
    stream = stream['source']
    fd = stream.open()
    print("CONNECTED!")
    f = open("stream.dat", 'wb')

    while True:
        data = fd.read(1024)
        f.write(data)
 
def twitch_chat():
    print "ABOUT TO JOIN TWITCH CHAT"

    HOST = "irc.twitch.tv"
    PORT = 6667
    NICK = "Vatyx"
    IDENT = "Vatyx"
    PASS = "oauth:rcfcmw3fpacgnqqzeu7igcxtyt63ed"
    REALNAME = "Vatyx"
    CHANNEL = "#" + channel
    readbuffer = ""

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS %s\r\n" % PASS)
    s.send("NICK %s\r\n" % NICK)
    s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
    s.send("JOIN %s\r\n" % CHANNEL)
    last_counts = [0, 0, 0]
    all_counts = [0] * 20
    counts_total = 0
    min_seconds = 20
    times = 0

    index = 0
    index2 = 0
    current = datetime.now()
    count = 0
    threshold = 5
    threshold_multiplier = 1.5
 
    set_start = False
    #set_end = False
    #interlude_count = 2

    print "JOINED!"
 
    while 1:
        if (datetime.now() - current).seconds >= 1:
            print "TIME:   " + str(datetime.now() - current) + " COUNT:    " + str(count) + " " + ("#" * count)
            temp = all_counts[index]
            all_counts[index] = count
            index = (index + 1) % 20

            last_counts[index2] = count
            index2 = (index2 + 1) % 3
            #all_counts.append(count)
            counts_total += count
            counts_total -= temp
            average_count = counts_total / float(20)
            print "THRESHOLD:   " + str(counts_total / float(20))
            # if not set_start and all(count >= threshold for count in last_counts):
            if not set_start and times >= min_seconds:
                #if all(count >= threshold_multiplier * average_count for count in all_counts[-4:-1]):
                if sum(last_counts) >= threshold_multiplier * average_count * 3:
                    set_start = True
                    start = front - EIGHT_SECONDS - DELAY
                    print ":twitch_chat START    =" + str(start) # printed start for debugging
                    print("~~~Highlight start set!~~~")

            elif set_start and times >= min_seconds:
                if all(count < threshold_multiplier * average_count for count in last_counts):
                    #set_end = True
                    end = front + FIVE_SECONDS - DELAY
                    print ":twitch_chat END    =" + str(end) # printed end for debugging
                    set_start = False
                    print("~~~Highlight end~~~")
                    threading.Timer(7.0, create_highlight).start()
 
            count = 0
            current = datetime.now()
            times += 1
 
        readbuffer = readbuffer + s.recv(1024)
        temp = string.split(readbuffer, "\r\n")
 
        readbuffer = temp.pop()
 
        for line in temp:
            line = string.rstrip(line)
            line = string.split(line)
            if (line[0] == "PING"):
                s.send("PONG %s\r\n" % line[1])


        count += 1
 
def main():
    # create_highlight()
    global channel

    # t2 = threading.Thread(target = stream_recording)
    # t2.start()
    # threads.append(t2)

    # t1 = threading.Thread(target = twitch_chat)
    # t1.start()
    # threads.append(t1)

    create_highlight(3, 7)
 

 
if __name__ == "__main__":
    main()