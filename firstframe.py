from livestreamer import Livestreamer
session = Livestreamer()
stream = session.streams('http://www.twitch.tv/starladder_cs_en')
print("connected")
stream = stream['source']
fd = stream.open()
print("done")

front = 0
rear = 0
with open("stream.dat", 'wb') as f:
	while front < 1024 * 6000:
		data = fd.read(1024)
        f.write(data)
        front += 1024
        print("writing")
	while True:
		if(front == 1024 * 12000):
			f.seek(0)
			front = 0
		if(rear == 1024 * 12000):
			rear = 0
		data = fd.read(1024)
		f.write(data)
		front += 1024
		rear += 1024
		print("writing")