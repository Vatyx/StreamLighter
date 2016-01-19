import socket
import sys
import string

HOST="irc.twitch.tv"
PORT=6667
NICK="vatyx"
IDENT="vatyx"
PASS= "oauth:v9h7fnm6uh7a8zy9v32gqivpt34mo6"
REALNAME = "vatyx"
CHANNEL = "#starladder1"
readbuffer = ""
msg = ""

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS %s\r\n" % PASS)
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("JOIN %s\r\n" % CHANNEL)

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\r\n")
    index = temp[0].find(":", 1) + 1
    msg = (temp[0])[index:]
    print(msg)
    readbuffer=temp.pop( )

    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)

        if(line[0]=="PING"):
            s.send("PONG %s\r\n" % line[1])