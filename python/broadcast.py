#!/usr/bin/python

# Send UDP broadcast packets

MYPORT = 50000 # Set some reasonable port
MYNET = '' # Must end with .255 (= broadcast)

import sys, time
import socket

# Helper functions
# Might be a bit of a hack, but seems to work ok

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]


def get_broadcast_address():
	ip_array = get_ip_address().split('.')
	ip_array[3] = "255"
	return '.'.join(ip_array)

# If defaults fail
def setup(ip, port):
	global MYPORT  
	global MYNET
	MYNET = ip
	MYPORT = port

# send
def send(msg):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.sendto(msg, (MYNET, MYPORT))

if __name__ != "__main__":
	# Imported
	MYNET = get_broadcast_address()
else:
	MYNET = get_broadcast_address()
	send(repr(time.time()))
