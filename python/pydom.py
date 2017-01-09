#!/usr/bin/env python3

import pydomoticz

import argparse

def set(args):
    pydomoticz.switchDevice(idx=args.idx, value=args.command)

def toggle(args):
    pydomoticz.toggleDevice(args.idx)

def scene(args):
    pydomoticz.activateScene(args.idx)

def list(args):
    print("List")

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", help="Commands")
subparsers.required = True

parser_set = subparsers.add_parser("set", help="Set switch On/Off")
parser_set.add_argument("idx")
parser_set.add_argument("command", choices=["On", "Off"])
parser_set.set_defaults(func=set)

parser_toggle = subparsers.add_parser("toggle", help="Toggle switch")
parser_toggle.add_argument("idx")
parser_toggle.set_defaults(func=toggle)

parser_scene = subparsers.add_parser("scene", help="List")
parser_scene.add_argument("idx")
parser_scene.set_defaults(func=scene)

parser_list = subparsers.add_parser("list", help="List")
parser_list.add_argument("type", choices=["devices", "scenes"])
parser_list.set_defaults(func=list)

args = parser.parse_args()

print (args.command)

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
