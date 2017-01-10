#!/usr/bin/env python3

import pydomoticz
import argparse

def setDevice(args):
    pydomoticz.setDevice(args.idx, args.command)

def toggleDevice(args):
    pydomoticz.toggleDevice(args.idx)

parser = pydomoticz.defultArgs()

subparsers = parser.add_subparsers(dest="command")
subparsers.required = True

parser_set = subparsers.add_parser("set")
parser_set.add_argument("idx")
parser_set.add_argument("command", choices=["On", "Off"])
parser_set.set_defaults(func = setDevice)

parser_toggle = subparsers.add_parser("toggle")
parser_toggle.add_argument("idx")
parser_toggle.set_defaults(func = toggleDevice)

args = parser.parse_args()
pydomoticz.setServerFromArgs(args)
args.func(args)
