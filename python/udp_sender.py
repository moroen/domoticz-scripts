#!/usr/bin/python

import udp
import argparse

parser = argparse.ArgumentParser(description='Listen to UDP-packets')

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('-b', "--broadcast", action='store_true', help="Send to broadcast")
group.add_argument("-a", "--address", default='', help="Address to send to. If not specified, try to figure local IP")
parser.add_argument("-p", "--port", default=5000, type=int, help="Port to send to. Default 5000")

parser.add_argument('-v', "--verbose", action='store_true')

parser.add_argument("message")
args = parser.parse_args()

if args.broadcast:
	ip = udp.get_broadcast_address()
elif args.address == '':
	ip = udp.get_ip_address()
else:
	ip = args.address

port = args.port  # where do you want to send a msg?
udp.setup(ip, port)
udp.send(args.message, args.verbose)
