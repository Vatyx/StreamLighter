import irc.client
import sys

class IRCCat(irc.client.SimpleIRCClient):
    def __init__(self, target):
        irc.client.SimpleIRCClient.__init__(self)
        self.target = target

    def on_welcome(self, connection, event):
        print("welcomed")
        print(event);
        if irc.client.is_channel(self.target):
            connection.join(self.target)
        # else:
        #     self.send_it()

    def _dispatcher(self, connection, event):
        """
        Dispatch events to on_<event.type> method, if present.
        """
        print("_dispatcher: %s", event.type)

        do_nothing = lambda c, e: None
        method = getattr(self, "on_" + event.type, do_nothing)
        method(connection, event)

    def on_all_raw_messages(self, connection, event):
        print("got here")

    def on_join(self, connection, event):
        pass
        #self.send_it()

    def on_disconnect(self, connection, event):
        sys.exit(0)

    def on_pubmsg(self, c, e):
        print("got in here")

    # def send_it(self):
    #     while 1:
    #         print("oh shit I got in here yes")
    #         break
    #     self.connection.quit("Using irc.client.py")

def main():
    if len(sys.argv) != 4:
        print("Usage: irccat2 <server[:port]> <nickname> <target>")
        print("\ntarget is a nickname or a channel.")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    nickname = sys.argv[2]
    target = sys.argv[3]

    c = IRCCat(target)
    try:
        print("About to connect")
        c.connect(server, port, nickname, "oauth:v9h7fnm6uh7a8zy9v32gqivpt34mo6")
        print("Success?")
    except irc.client.ServerConnectionError as x:
        print(x)
        sys.exit(1)
    c.start()
    print("Reached end of file")

if __name__ == "__main__":
    main()