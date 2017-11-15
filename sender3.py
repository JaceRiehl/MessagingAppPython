#!/usr/bin/python

# A simple UDP datagram sender 

import sys,socket

PORT=55000
#DESTIP="142.66.140.13"  # linux1.cs

if len(sys.argv) != 2:
    print("Usage: {} destination_IP_addr".format(sys.argv[0])) 
    sys.exit(1)

try:
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
    print("Cannot open socket")
    sys.exit(1)

# try:
#     s.bind(('',PORT+1))
# except:
#     print("Cannot bind socket to port")
#     sys.exit(1)

try:
    # can also use bytes('Hello world', 'UTF-8')
    s.sendto(b'Hello world', (sys.argv[1], PORT))
except OSError as err:
    print('Cannot send: {}'.format(err.strerror))
    sys.exit(1)
