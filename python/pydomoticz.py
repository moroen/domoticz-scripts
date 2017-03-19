#!/usr/bin/env python3

import base64
import sys
import json

import urllib.request as urllib2
import collections
import argparse

from urllib.parse import quote


isVerbose = False

domoticzserver = "127.0.0.1:8080"
domoticzusername = ""
domoticzpassword = ""
awayDeviceName = "Away"
base64string = base64.encodestring(bytes(('%s:%s' % (domoticzusername, domoticzpassword)).replace('\n', ''), 'utf-8'))

currentScenes = {}

def defaultArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "-s", "--server", default="127.0.0.1")
    parser.add_argument("--port", default="8080")

    return parser

def getServerInfo():
    global domoticzserver
    return domoticzserver

def setServerFromArgs(args):
    global domoticzserver
    domoticzserver = "{0}:{1}".format(args.host, args.port)

def setServer(host, port):
    global domoticzserver
    domoticzserver = "{0}:{1}".format(host, port)

def DomoticzRequest(params):
    global domoticzserver

    url = "http://{0}/json.htm?{1}".format(domoticzserver, params)

    if isVerbose:
        print (url)

    request = urllib2.Request(url)
    request.add_header("Authorization", "Basic %s" % base64string)
    try:
        response = urllib2.urlopen(request)
        return json.loads(response.read().decode('utf-8'))

    except urllib2.URLError:
        print ("Error - Couldn't open URL")
        return None


def getScenesFromServer():
    params = "filter=all&order=Name&type=scenes&used=true"

    global currentScenes
    currentScenes = {}

    res = DomoticzRequest(params)

    if res != None:
        currentScenes = [aScene for aScene in res['result']]
            # newGroups = [aScene for aScene in DomoticzRequest(params)['result'] if aScene['Type']=='Group']
    else:
        currentScenes = None

# Devices
def getDevice(idx):
    params = "type=devices&rid={0}".format(idx)
    res = DomoticzRequest(params)
    return res["result"][0]

def getAllDevices(filter=None):
    pass

# Device functions
def setDevice(idx, value):
    param = "type=command&param=switchlight&idx={0}&switchcmd={1}".format(idx, value)
    res = DomoticzRequest(param)

def setDeviceLevel(idx, level):
    param = "type=command&param=switchlight&idx={0}&switchcmd=Set%20Level&level={1}".format(idx, level)
    res = DomoticzRequest(param)

def toggleDevice(idx):
    """Toggle the device"""
    dev = getDevice(idx)
    if dev["Status"] == "Off":
        setDevice(idx, "On")
    else:
        setDevice(idx, "Off")

def setDeviceToHigh(idx):
    dev = getDevice(idx)
    valName = "{0}_High".format(dev["Name"])
    val = getVariable(valName, 90)
    setDeviceLevel(idx, val)

def setDeviceToLow(idx):
    dev = getDevice(idx)
    valName = "{0}_Low".format(dev["Name"])
    val = getVariable(valName, 90)
    setDeviceLevel(idx, val)

def toggleDeviceHighLow(idx):
    dev = getDevice(idx)
    lowLevel = int(getVariable("{0}_Low".format(dev["Name"]), 50))
    highLevel = int(getVariable("{0}_High".format(dev["Name"]), 50))
    currentLevel = int(dev["LevelInt"])+1

    if currentLevel < lowLevel:
        targetLevel = lowLevel
    elif currentLevel >= lowLevel and currentLevel < highLevel:
        targetLevel = highLevel
    elif currentLevel >= highLevel:
        targetLevel = lowLevel

    if isVerbose:
        print("Current: ", currentLevel, "low: ", lowLevel, "High: ", highLevel)
        print("Setting to: ", targetLevel)

    setDeviceLevel(idx=idx, level=targetLevel)

# Scenes functions
def activateScene(idx):
    param = "type=command&param=switchscene&idx={0}&switchcmd=On".format(idx)
    res = DomoticzRequest(param)


def getScenes(type="Scene", forceReload=False):
    global currentScenes

    if (not currentScenes) or (forceReload):
        getScenesFromServer()

    if currentScenes:
        return sorted([aScene for aScene in currentScenes if aScene['Type']==type], key=lambda scene: scene['Name'])

# Variables

def setVariable(name, value):

    value = str(value)

    param = "type=command&param=updateuservariable&vname={0}&vtype=2&vvalue={1}".format(quote(name), quote(value))
    res = DomoticzRequest(param)

    if res['status'] == "ERR":
        param = "type=command&param=saveuservariable&vname={0}&vtype=2&vvalue={1}".format(quote(name), quote(value))
        res = DomoticzRequest(param)

    return res

def getVariable(name, defaultValue = None, Create = False):
    param = "type=command&param=getuservariables"
    res = DomoticzRequest(param)

    if res['status'] == "OK":
        for aRes in res['result']:
            if aRes['Name'] == name:
                return aRes['Value']

    # Not found
    if defaultValue != None:
        if Create:
            setVariable(name, defaultValue)
        return defaultValue

    return None

if __name__ == '__main__':
    print ("Pydomoticz v0.1")
    print (sys.version)

    #data = getScenes()
    #print (data[0])

    dev = getDevice(2)
    print (dev["Name"])

else:
    domoticzserver = getServerInfo()
