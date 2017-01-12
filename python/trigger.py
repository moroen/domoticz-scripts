#!/usr/bin/env python3

import shelve
import time

import pydomoticz
import argparse

parser = pydomoticz.defultArgs()

class triggerInfo():
    pass
parser.add_argument('state')
parser.add_argument('idx')

args = parser.parse_args()

n = triggerInfo()
n.time = time.time()

with shelve.open('triggers') as db:
    #db["test"] = n
    #db['1'] = n

    if args.state == "On":
        tm = time.time()
        print("Setting to: {0}".format(tm))
        n.time = tm
        db[args.idx] = n
        
    elif args.state == "Off":
        if args.idx in db:
            print (db[args.idx].time)
