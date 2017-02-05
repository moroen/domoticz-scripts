#!/usr/bin/env python3

import shelve
import time

import pydomoticz
import argparse

longClickDuration = 2

parser = pydomoticz.defultArgs()

class triggerInfo():
    pass

parser.add_argument('state', choices=['On', 'Off', 'Setup'])
parser.add_argument('idx')

args = parser.parse_args()

pydomoticz.setServerFromArgs(args)

targetDevice = pydomoticz.getDevice(args.idx)

with shelve.open('triggers') as db:
    #db["test"] = n
    #db['1'] = n

    if args.state == "On":
        tm = time.time()
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
                print("longer")
                pydomoticz.setDeviceLevel(args.idx, 10)
            else:
                print("Shorter")
                pydomoticz.toggleDevice(args.idx)

    elif args.state == "Setup":
        # print(targetDevice['Name'])
        # pydomoticz.setVariable("{0}_high".format(targetDevice['Name']), "99")
        valueHigh = pydomoticz.getVariable("{0}_high".format(targetDevice['Name']), 99, True)
        valueLow = pydomoticz.getVariable("{0}_low".format(targetDevice['Name']), 50, True)
        #print (value)
