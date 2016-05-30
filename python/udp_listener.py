#!/usr/bin/python

import select, socket, sys, argparse
import udp

parser = argparse.ArgumentParser(description='Listen to UDP-packets')

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('-b', "--broadcast", action='store_true', help="Listen for broadcast")
group.add_argument("-a", "--address", default='', help="Address to listen to. If not specified, try to figure local IP")

parser.add_argument("-p", "--port", default=5000, type=int, help="Port to listen to. Default 5000")

parser.add_argument('-v', "--verbose", action='store_true')

args = parser.parse_args()

port = args.port  # where do you expect to get a msg?
#netbroadcast = args.address # must end with 255 (=broadcast)
bufferSize = 1024 # whatever you need

if args.broadcast:
	ip = udp.get_broadcast_address()
elif args.address == '':
	ip = udp.get_ip_address()
else:
	ip = args.address

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((ip, port))
	s.setblocking(0)

	if args.verbose:
		print "Listening on " + ip + ":" + str(port)

	while True:
		result = select.select([s],[],[])
		msg = result[0][0].recv(bufferSize)
		print msg

except KeyboardInterrupt:
	print "Done"
except:
	print "Error: Unable to bind to " + ip + ":" + str(port)