#!/usr/bin/env python3

import base64
import sys
import json

import urllib.request as urllib2
import collections

# import kivy.config as config

# from kivy.config import ConfigParser

domoticzserver = "zwave:8080"
domoticzusername = ""
domoticzpassword = ""
awayDeviceName = "Away"
base64string = base64.encodestring(bytes(('%s:%s' % (domoticzusername, domoticzpassword)).replace('\n', ''), 'utf-8'))

currentScenes = {}

def getServerInfo():
    global domoticzserver
    return domoticzserver

def DomoticzRequest(params):
    global domoticzserver

    url = "http://{0}/json.htm?{1}".format(domoticzserver, params)

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

def switchDevice(idx, value):
    param = "type=command&param=switchlight&idx={0}&switchcmd={1}".format(idx, value)
    res = DomoticzRequest(param)

def toggleDevice(idx):
    """Toggle the device"""
    dev = getDevice(idx)
    if dev["Status"] == "Off":
        switchDevice(idx, "On")
    else:
        switchDevice(idx, "Off")

def activateScene(idx):
    param = "type=command&param=switchscene&idx={0}&switchcmd=On".format(idx)
    res = DomoticzRequest(param)

def getDevice(idx):
    params = "type=devices&rid={0}".format(idx)
    res = DomoticzRequest(params)
    return res["result"][0]

def getScenes(type="Scene", forceReload=False):
    global currentScenes

    if (not currentScenes) or (forceReload):
        getScenesFromServer()

    if currentScenes:
        return sorted([aScene for aScene in currentScenes if aScene['Type']==type], key=lambda scene: scene['Name'])

if __name__ == '__main__':
    print ("pydomoticz standalone")
    print (sys.version)

    #data = getScenes()
    #print (data[0])

    dev = getDevice(2)
    print (dev["Name"])

else:
    print ("pydomoticz module")
    domoticzserver = getServerInfo()
