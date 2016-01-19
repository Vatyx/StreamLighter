import threading
import time
import sys

print("hi")

channel = "dreadztv"
 
EIGHT_SECONDS = 4500000
FIVE_SECONDS = 3700000
DELAY = 13000000
 
threads = []
 
front = 0
 
start = 0
end = 0


 
def create_highlight():
    import time

    global start
    global end
 
    print("creating highlight")
    
    stream = open("stream.dat", 'rb')
    stream.seek(start)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    highlight = open("highlight-" + timestr + ".dat", 'wb')
    buffer = stream.read(end - start)
    print(len(buffer))

    highlight.write(buffer)

    stream.close()
    highlight.close()

    print "highlight-" + timestr + ".dat"
 
def stream_recording():
    from livestreamer import Livestreamer
 
    print(": Starting to record stream")
 
    session = Livestreamer()
    stream = session.streams('http://www.twitch.tv/' + channel)
    print("Connecting to stream")
    stream = stream['source']
    fd = stream.open()
    print("Connected!")
    lock = threading.Lock()
    f = open("stream.dat", 'wb')# with open("stream.dat", 'wb') as f:
    #start_time = time.time()
    global front
    while True:
        data = fd.read(1024)
        f.write(data)
        front += len(data)
        #print "--- %s seconds ---" % (time.time() - start_time)
        #print("Stream recording: front " + str(front))

    lock.release()
 
def twitch_chat():
    print "Just entered twitch_chat"
    sys.stdout.flush()
    import socket
    import string
    from datetime import datetime

    HOST = "irc.twitch.tv"
    PORT = 6667
    NICK = "him229"
    IDENT = "him229"
    PASS = "oauth:s5gbwbjaj61bb95zfbtaxrgnyv0ssr"
    REALNAME = "him229"
    CHANNEL = "#" + channel
    readbuffer = ""
    global start
    global end
    print("got here")
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS %s\r\n" % PASS)
    s.send("NICK %s\r\n" % NICK)
    s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
    s.send("JOIN %s\r\n" % CHANNEL)
    print("and here")
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
    threshold_multiplier = 1.3
 
    set_start = False
    #set_end = False
    #interlude_count = 2

    print ": before while twitch_chat"
    sys.stdout.flush()
 
    while 1:
        if (datetime.now() - current).seconds >= 1:
            print "TIME:   " + str(datetime.now() - current) + " COUNT:    " + str(count) + " " + ("#" * count)
            sys.stdout.flush()
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
            sys.stdout.flush()
            # if not set_start and all(count >= threshold for count in last_counts):
            if not set_start and times >= min_seconds:
                #if all(count >= threshold_multiplier * average_count for count in all_counts[-4:-1]):
                print("Im in here testing")
                if sum(last_counts) >= threshold_multiplier * average_count * 3:
                    set_start = True
                    start = front - EIGHT_SECONDS - DELAY
                    print ":twitch_chat START    =" + str(start) # printed start for debugging
                    sys.stdout.flush()
                    print("~~~Highlight start set!~~~")
                    sys.stdout.flush()
            # elif interlude_count != 0:
            #     print("Interlude")
            #     interlude_count -= 1
            elif set_start and times >= min_seconds:
                if all(count < threshold_multiplier * average_count for count in last_counts):
                    #set_end = True
                    end = front + FIVE_SECONDS - DELAY
                    print ":twitch_chat END    =" + str(end) # printed end for debugging
                    sys.stdout.flush()
                    set_start = False
                    print("~~~Highlight end~~~")
                    sys.stdout.flush()
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
    channel = raw_input("Hi there")
    print("Channel to record is " + channel)
    sys.stdout.flush()

    t2 = threading.Thread(target = stream_recording)
    t2.start()
    threads.append(t2)

    t1 = threading.Thread(target = twitch_chat)
    t1.start()
    threads.append(t1)
 

 
if __name__ == "__main__":
    main()