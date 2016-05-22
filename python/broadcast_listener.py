#!/usr/bin/python

import select, socket, sys, argparse
import broadcast

parser = argparse.ArgumentParser(description='Listen to UDP-broadcasts')
parser.add_argument("-a", "--address", default='', help="Address to listen to. If not specified, try to figure out broadcast")
parser.add_argument("-p", "--port", default=50000, type=int, help="Port to listen to. Default 50000")
args = parser.parse_args()

port = args.port  # where do you expect to get a msg?
#netbroadcast = args.address # must end with 255 (=broadcast)
bufferSize = 1024 # whatever you need


if args.address == '':
	netbroadcast = broadcast.get_broadcast_address()
else:
	netbroadcast = args.address # must end with 255 (=broadcast)

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((netbroadcast, port))
	s.setblocking(0)

	if netbroadcast == '':
		print "Listening on port " + str(port)
	else:
		print "Listening on " + netbroadcast + ":" + str(port)

	while True:
		result = select.select([s],[],[])
		msg = result[0][0].recv(bufferSize)
		print msg

except KeyboardInterrupt:
	print "Done"
except:
	print "Error: Unable to bind to " + netbroadcast + ":" + str(port)