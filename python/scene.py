#!/usr/bin/env python3

import pydomoticz
import argparse

parser = pydomoticz.defultArgs()

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


subparsers = parser.add_subparsers(dest="command")
subparsers.required = True

parser_set = subparsers.add_parser("activate")
parser_set.add_argument("idx")
parser_set.set_defaults(func = scenes)

parser_list = subparsers.add_parser("list")
parser_list.set_defaults(func = scenes)

args = parser.parse_args()
pydomoticz.setServerFromArgs(args)
args.func(args)
