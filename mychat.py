import sys,socket,errno 
from queue import Queue,Empty
from threading import *
from time import sleep
import os

BUFLEN=1000
PORTS = [55000, 55001, 55002, 55003, 55004, 55005, 55006, 55007, 55008];
IPADDRESSES = [];

PEERLIST = []

try:
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
	print("Cannot open socket")
	sys.exit(1)

sourcePort = 55000
while(True):
	try:	
		s.bind(('', sourcePort))
	except:
		sourcePort += 1
		if(sourcePort > 55008):
			print("Cannot bind socket to port")
			sys.exit(1)
		continue
	break

## <---------- All Classes go here ----------> ##
class Receiver(Thread):
	def __init__(self, queue, s, userName):
		Thread.__init__(self)
		self.queue = queue
		self.s = s
		self.userName = userName

	def run(self):
		# i=0
		while True:
			data,addr = self.s.recvfrom(BUFLEN)
			if(data.decode()[0:5] == 'HELLO'):
				if(isNewUser(addr[0], addr[1])):
					index = 0
					if(data.decode()[5] == ' '):
						index = 6
					else:
						index = 5
					PEERLIST.append(Peer(data.decode()[index:], addr[0], addr[1]))
					if(len(PEERLIST) > 1):
						print(data.decode()[index:] + ' is online.')
			else:
				self.queue.put((data.decode(), addr))
				user = matchUser(addr[0], addr[1])
				if(user != self.userName):
					print(user + ': ' + data.decode())

class Peer(Thread):
	def __init__(self, userName, ip, port):
		Thread.__init__(self)
		self.userName = userName
		self.ip = ip
		self.port = port		
		self.isExpired = False
		self.t = Timer(15.0, self.expire) 
		self.t.start()

	def printInfo(self):
		print(self.userName + self.ip + str(self.port))

	def expire(self):
		self.isExpired = True

	def resetTimer(self):
		self.isExpired = False
		self.t.cancel()
		self.t = Timer(15.0, self.expire)
		self.t.start()

class Online(Thread):
	def __init__(self, user):
		Thread.__init__(self)
		self.user = user

	def run(self):
		while(True):
			for peers in PEERLIST:
				appendUser = 'HELLO'+user
				s.sendto(appendUser.encode(), (peers.ip, peers.port))
			sleep(5)

class UpdatePeers(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		while(True):
			tmpList = []
			i = 0
			for peers in PEERLIST:
				if(peers.isExpired):
					tmpList.append(i)
				i += 1
			for items in tmpList:
				print(PEERLIST[items].userName + ' has logged off...')
				del PEERLIST[items]
			sleep(5)

## <---------- End of Classes Declaration ----------> ##

def initialHELLO(userName):
	addIPs("142.66.140.",21,69);
	# addIPs("142.66.140.",46,69);
	addIPs("142.66.140.",186,186);
	for ip in IPADDRESSES:
		for port in PORTS:
			appendUser = 'HELLO'+userName
			s.sendto(appendUser.encode(), (ip, port))
			sleep(0.002)

def getUserName():
	if len(sys.argv) == 2:
		userName = sys.argv[1]
		uppers = [l for l in userName if l.isupper()]
		while((('-' not in userName) and ('_' not in userName) and ('.' not in userName)) or (len(uppers) == 0) or (len(uppers) == len(userName)) or (' ' in userName)):
			print("Invalid username, please try again")
			print('Input a username containing an uppercase, lowercase, and at least one of the follow characters: -, _, or .')
			userName = input('- ');
			uppers = [l for l in userName if l.isupper()];
	else:
		print('Input a username containing an uppercase, lowercase, and at least one of the follow characters: -, _, or .')
		userName = input('- ');
		uppers = [l for l in userName if l.isupper()]

		while((('-' not in userName) and ('_' not in userName) and ('.' not in userName)) or (len(uppers) == 0) or (len(uppers) == len(userName)) or (' ' in userName)):
			print("Invalid username, please try again")
			userName = input('- ');
			uppers = [l for l in userName if l.isupper()];

	return userName

def matchUser(address, port):
	for peers in PEERLIST:
		if(address == peers.ip and port == peers.port):
			return peers.userName
	return address

def isNewUser(ip, port):
	for peers in PEERLIST:
		if(peers.ip == ip and peers.port == port):
			peers.resetTimer()
			return False
	return True

def addIPs(base, start, end):
	i = start;
	while(i <= end):
		IPADDRESSES.append(base + str(i));
		i += 1;


def main(userName):
	print('\nWelcome to the messaging app')
	print('you are logged in as ' + userName);
	# Create a queue to communicate with the worker threads
	queue = Queue()
	# Create one daemon to receive messages (currently a fake receiver)
	receiver = Receiver(queue, s, userName)
	# Setting daemon to True will let the main thread exit even though the workers are blocking
	receiver.daemon = True
	receiver.start()
	iAmOnline = Online(userName)
	iAmOnline.daemon = True
	iAmOnline.start()
	updatePeers = UpdatePeers()
	updatePeers.daemon = True
	updatePeers.start()

	print(
		#'p - prints received messages\n
		's <msg> - sends message\nq - quits\n')
	cmd = input('')
	while (cmd != ('q' or 'Q')):
		if (cmd == ''):
			cmd = input('')
			continue
		# if (cmd[0] == ('p' or 'P')):
		# 	try:
		# 		while (True):
		# 			msg = queue.get(False,None)
		# 			print(matchUser(msg[1][0], msg[1][1]) + ': ' + msg[0])
		# 	except Empty:
		# 		print('------------------------------')
		if (cmd[0] == ('s' or 'S')):
			if(cmd[1] != ' '):
				message = cmd[1:]
			else:
				message = cmd[2:]
			try:
				for peers in PEERLIST:
					s.sendto(message.encode(), (peers.ip, peers.port))
			except OSError as err:
				print('Cannot send: {}'.format(err.strerror))
				sys.exit(1)

		if (cmd == 'list'):
			print("**** Current Users Online ****\n")
			for peers in PEERLIST:
				print(peers.userName + " " + peers.ip + ' ' + str(peers.port))
			print('\n')

		if(cmd == 'clear'):
			os.system('clear')
			print('s <msg> - sends message\nq - quits\n')
		cmd = input('')

	print('Baby come back...')

user = getUserName()	
initialHELLO(user)
main(user)
