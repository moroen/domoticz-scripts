#!/usr/bin/env python3

import pydomoticz

import argparse

def set(args):
    pydomoticz.switchDevice(idx=args.idx, value=args.command)

def toggle(args):
    pydomoticz.toggleDevice(args.idx)

def devices(args):
    print (args.command)

def scenes(args):
    print (args.command)
    if args.command == "activate":
        pydomoticz.activateScene(args.idx)
    elif args.command == "list":
        scenes = pydomoticz.getScenes()

        print ("Scenes:")
        for aScene in scenes:
            print ("{0}: {1}".format(aScene["idx"], aScene["Name"]))

        print ("\nGroups:")
        scenes = pydomoticz.getScenes(type="Group")
        for aScene in scenes:
            print ("{0}: {1}".format(aScene["idx"], aScene["Name"]))


#def listScenes(args):
#    print ("listScenes")

def list(args):
    print("List")

parser = argparse.ArgumentParser()
parser.add_argument("--host", "-s", "--server", default="127.0.0.1")
parser.add_argument("--port", default="8080")


subparsers = parser.add_subparsers(dest="command", help="Commands")
subparsers.required = True

parser_devices = subparsers.add_parser("devices", help = "Devices")
parser_devices.set_defaults(func=devices)


parser_scenes = subparsers.add_parser("scenes", help = "Scenes")
parser_scenes.set_defaults(func = scenes)

scenesubs = parser_scenes.add_subparsers(dest="command", help="Operations on Scenes")
scenesubs.required = True
scenesubs.add_parser("list")
sceneact_parser = scenesubs.add_parser("activate")
sceneact_parser.add_argument("idx")

#scenes.add_parser("list", help="Scene")


# parser_set = parser_device.add_subparser("set", help="Set switch On/Off")
# parser_set.add_argument("idx")
# parser_set.add_argument("command", choices=["On", "Off"])
# parser_set.set_defaults(func=set)
#
# parser_toggle = subparsers.add_parser("toggle", help="Toggle switch")
# parser_toggle.add_argument("idx")
# parser_toggle.set_defaults(func=toggle)
#
#
# parser_scenes = subparsers.add_parser("scenes", help="Scenes")
#
# scenesubs = parser_scenes.add_subparsers(dest="command", help="Scene")
# scenesubs.required = True
# scenelist_parser = scenesubs.add_parser("list", help="List scenes")
# sceneact_parser = scenesubs.add_parser("activate", help="Activate scene")
# sceneact_parser.add_argument("idx")
# parser_scenes.set_defaults(func = scenes)

args = parser.parse_args()

pydomoticz.setServer(args.host, args.port)

args.func(args)


# def switchDevice():
#     global parser
#
#
#     pydomoticz.switchDevice(1, "On")
#
# def toggleDevice():
#     print ("Toggle")
#
# def parseCommand(command):
#     return {
#         "set": switchDevice,
#         "toggle": toggleDevice,
#     }.get(command, 0)
#
# parseCommand(args.cmd)()
