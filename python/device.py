#!/usr/bin/env python3

import pydomoticz
import argparse

def setDevice(args):
    pydomoticz.setDevice(args.idx, args.command)

def toggleDevice(args):
    pydomoticz.toggleDevice(args.idx)

def setDeviceHighOrLow(args):
    if args.level:
        dev = pydomoticz.getDevice(args.idx)
        valName = "{0}_{1}".format(dev["Name"], args.command)

        pydomoticz.setVariable(valName, args.level[0])

    if args.command == "High":
        pydomoticz.setDeviceToHigh(args.idx)
    else:
        pydomoticz.setDeviceToLow(args.idx)

parser = pydomoticz.defaultArgs()


parser.add_argument("command", choices=["On", "Off", "Toggle", "High", "Low", "ToggleHighLow"], help="Command")
parser.add_argument("idx", help="Device ID")

parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
parser.add_argument("--level", nargs=1, help="Level for On, High, Low")


args = parser.parse_args()
pydomoticz.setServerFromArgs(args)

if args.verbose:
    pydomoticz.isVerbose=True
    print(args.idx, args.command)

if args.command == "On":
    if args.level:
        print ("Level: ", args.level[0])
        pydomoticz.setDeviceLevel(args.idx, args.level[0])
    else:
        pydomoticz.setDevice(args.idx, "On")

elif args.command == "Off":
    pydomoticz.setDevice(args.idx, "Off")

elif args.command == "Toggle":
    pydomoticz.toggleDevice(args.idx)

elif args.command == "High" or args.command == "Low":
    setDeviceHighOrLow(args)

elif args.command == "ToggleHighLow":
    pydomoticz.toggleDeviceHighLow(args.idx)
