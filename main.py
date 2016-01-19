import threading
 

 # 27753868
 #22220172
channel = "showdownsmash2"
 
EIGHT_SECONDS = 4500000
FIVE_SECONDS = 3700000
DELAY = 4600000
 
threads = []
 
front = 0
 
start = 162906888
end = 174920172

threshold = 10


 
def create_highlight():
    import time

    global start
    global end
 
    print("creating highlight")
    
    stream = open("stream.dat", 'rb')
    stream.seek(start)
    print(stream)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    highlight = open("highlight-" + timestr + ".dat", 'wb')
    print(highlight)
    buffer = stream.read(end - start)
    print(len(buffer))

    highlight.write(buffer)

    stream.close()
    highlight.close()
 
def stream_recording():
    from livestreamer import Livestreamer
 
    print(": Starting to record stream")
 
    session = Livestreamer()
    stream = session.streams('http://www.twitch.tv/' + channel)
    print("Connecting to stream")
    stream = stream['source']
    fd = stream.open()
    print("Connected!")

    #lock = threading.Lock()
    f = open("stream.dat", 'wb')# with open("stream.dat", 'wb') as f:

    global front
    while True:
        data = fd.read(1024)
        f.write(data)
        front += len(data)
        #print("Stream recording: front " + str(front))

    #lock.release()
 
def twitch_chat():
    print "Just entered twitch_chat"
    import socket
    import sys
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
 
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS %s\r\n" % PASS)
    s.send("NICK %s\r\n" % NICK)
    s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
    s.send("JOIN %s\r\n" % CHANNEL)
    last_counts = [0, 0, 0]
    index = 0
    current = datetime.now()
    count = 0
 
    set_start = False
    #set_end = False
    #interlude_count = 2

    print ": before while twitch_chat"
 
    while 1:
 
        if (datetime.now() - current).seconds >= 1:
            print "TIME:   " + str(datetime.now() - current) + " COUNT:    " + str(count) + " " + ("#" * count)
            last_counts[index] = count
            index = (index + 1) % 3
            if not set_start and all(count >= threshold for count in last_counts):
                set_start = True
                start = front - EIGHT_SECONDS - DELAY
                print ":twitch_chat START    =" + str(start) # printed start for debugging
                print ":twitch_chat FRONT    =" + str(front)
                print("~~~Highlight start set!~~~")
            # elif interlude_count != 0:
            #     print("Interlude")
            #     interlude_count -= 1
            elif set_start and all(count < threshold for count in last_counts):
                #set_end = True
                end = front + FIVE_SECONDS - DELAY
                print ":twitch_chat END    =" + str(end) # printed end for debugging
                set_start = False
                print("~~~Highlight end~~~")
                threading.Timer(7.0, create_highlight).start()
 
            count = 0
            current = datetime.now()
 
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
    #create_highlight()

    t2 = threading.Thread(target = stream_recording)
    t2.start()
    threads.append(t2)

    t1 = threading.Thread(target = twitch_chat)
    t1.start()
    threads.append(t1)
 

 
if __name__ == "__main__":
    main()