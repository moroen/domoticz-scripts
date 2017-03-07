#!/usr/bin/env python3

import shelve
import time

import pydomoticz
import argparse

longClickDuration = 2

parser = pydomoticz.defaultArgs()

class triggerInfo():
    pass

parser.add_argument('state', choices=['On', 'Off'])
parser.add_argument('idx')
parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

args = parser.parse_args()
pydomoticz.setServerFromArgs(args)

if args.verbose:
    pydomoticz.isVerbose=True

targetDevice = pydomoticz.getDevice(args.idx)

with shelve.open('triggers') as db:
    #db["test"] = n
    #db['1'] = n

    if args.state == "On":
        tm = time.time()

        if pydomoticz.isVerbose:
            print("Setting to: {0}".format(tm))

        if args.idx in db:
            n = db[args.idx]
        else:
            n = triggerInfo()

        n.time = tm
        db[args.idx] = n

    elif args.state == "Off":
        if args.idx in db:
            n = db[args.idx]
            offTime = time.time()
            delta = offTime - n.time

            if delta > longClickDuration:
                if pydomoticz.isVerbose:
                    print("Long Click")
                pydomoticz.toggleDeviceHighLow(args.idx)
            else:
                if pydomoticz.isVerbose:
                    print("Short Click")
                pydomoticz.toggleDevice(args.idx)
