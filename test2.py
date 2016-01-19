import socket
import sys
import string
import matplotlib.pyplot as plt
from datetime import datetime
import urllib2
import threading
import thread



threads = []

def twitchchat():
    HOST="irc.twitch.tv"
    PORT=6667
    NICK="him229"
    IDENT="him229"
    PASS= "oauth:s5gbwbjaj61bb95zfbtaxrgnyv0ssr"
    REALNAME = "him229"
    CHANNEL = "#starladder1"
    readbuffer = ""
    msg = ""

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS %s\r\n" % PASS)
    s.send("NICK %s\r\n" % NICK)
    s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
    s.send("JOIN %s\r\n" % CHANNEL)
    number_of_messages=[]
    time=[]
    current = datetime.now()
    count = 0
    while 1:

        if (datetime.now() - current).seconds >= 1:  
            print "TIME:   " + str(datetime.now() - current) + " COUNT:    " + str(count) + " " + ("#"*count) 
            count = 0
            current = datetime.now()
        
        readbuffer=readbuffer+s.recv(1024)
        temp=string.split(readbuffer, "\r\n")
        index = temp[0].find(":", 1) 
        msg = (temp[0])[index+1:]
        #print(msg)

        # plt.plot(time,number_of_messages)
        # plt.show()

        readbuffer=temp.pop( )

        for line in temp:
            line=string.rstrip(line)
            line=string.split(line)
            if(line[0]=="PING"):
                s.send("PONG %s\r\n" % line[1])
        count+=1

def main():
    t = threading.Thread(target=twitchchat)
    threads.append(t)
    t.start()

if __name__ == "__main__":
    main()
