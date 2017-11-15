#!/usr/bin/python3

# a simple udp receiver (server)

import socket,sys,errno

PORT=55000
BUFLEN=1000

try:
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
    print("Cannot open socket")
    sys.exit(1)

try:
    s.bind(('12.34.64.76',PORT))
except:
    print("Cannot bind socket to port")
    sys.exit(1)

try:
    data,addr = s.recvfrom(BUFLEN)
except OSError as err:
    print("Cannot receive from socket: {}".format(err.strerror))
    sys.exit(1)

print("Received {} from {}".format(data, addr))
