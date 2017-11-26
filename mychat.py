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

	#Input userName 

	print('Input a username containing an uppercase, lowercase, and at least one of the follow characters: -, _, or .')

	userName = input('- ');
	uppers = [l for l in userName if l.isupper()]
	# if(len(uppers) == 0):
	# 	print("No uppers in here");
	#userName.find('-') == -1) or (userName.find('_') == -1) or (userName.find('.') == -1)
	while((('-' not in userName) and ('_' not in userName) and ('.' not in userName)) or (len(uppers) == 0) or (len(uppers) == len(userName)) or (' ' in userName)):
		userName = input('- ');
		uppers = [l for l in userName if l.isupper()];

	print('HELLO ' + userName);
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
	cmd = input('- ')
	while (cmd[0] != ('q' or 'Q')):
		if (cmd[0] == ('p' or 'P')):
			try:
				while (True):
					msg = queue.get(False,None)
					print(msg)
			except Empty:
				print('------------------------------')

		if (cmd[0] == ('s' or 'S')):
			
			if(cmd[1] != ' '):
				message = cmd[1:]
			else:
				message = cmd[2:]
			try:
				s.sendto(message.encode(), (peerIPAddr, peerPort))
			except OSError as err:
				print('Cannot send: {}'.format(err.strerror))
				sys.exit(1)
		cmd = input('& ')


	print('Baby come back...')
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
