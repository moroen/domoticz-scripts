#!/usr/bin/python

# Send UDP broadcast packets

MYPORT = 50000
MYNET = '192.168.1.255' # Must end with .255 (= broadcast)

import sys, time
from socket import *

def setup(ip, port):
	global MYPORT  
	global MYNET
	MYNET = ip
	MYPORT = port

def send(msg):
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	s.sendto(msg, (MYNET, MYPORT))

