import os 
import sys,socket,errno 
from queue import Queue,Empty
from threading import Thread
from time import sleep

BUFLEN=1000

class Receiver(Thread):
	def __init__(self, queue, s):
		Thread.__init__(self)
		self.queue = queue
		self.s = s
		


	def run(self):
		i=0
		while True:
			data,addr = self.s.recvfrom(BUFLEN)
			self.queue.put(data.decode())


def main():
	if len(sys.argv) != 4:
	    print("Usage: {} destination_IP_addr".format(sys.argv[0])) 
	    sys.exit(1)

	sourcePort = int(sys.argv[1])
	peerIPAddr = sys.argv[2]
	peerPort = int(sys.argv[3])


	try:
		s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	except:
		print("Cannot open socket")
		sys.exit(1)

	try:
		s.bind(('',sourcePort))
	except:
		print("Cannot bind socket to port")
		sys.exit(1)


	# Create a queue to communicate with the worker threads
	queue = Queue()
	   # Create one daemon to receive messages (currently a fake receiver)
	receiver = Receiver(queue,s)
	   # Setting daemon to True will let the main thread exit even though the workers are blocking
	receiver.daemon = True
	receiver.start()



	print('p - prints received messages\ns <msg> - sends message\nq - quits\n')
	cmd = input('& ')
	while (cmd[0] != 'q'):
		if (cmd[0] == 'p'):
			try:
				while (True):
					msg = queue.get(False,None)
					print(msg)
			except Empty:
				print('---')

		if (cmd[0] == 's'):
			message = cmd[2:]
			try:
				s.sendto(message.encode(), (peerIPAddr, peerPort))
			except OSError as err:
				print('Cannot send: {}'.format(err.strerror))
				sys.exit(1)
		cmd = input('& ')


	print('Bye...')
main()








# try:
#     s.bind(('',sourcePort))
# except:
#     print("Cannot bind socket to port")
#     sys.exit(1)

# try:
#     # can also use bytes('Hello world', 'UTF-8')
#     s.sendto(b'Hello world', (peerIPAddr, peerPort))
# except OSError as err:
#     print('Cannot send: {}'.format(err.strerror))
#     sys.exit(1)
