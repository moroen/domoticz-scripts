#!//usr/bin/python

# Domoticz Pyhton script for enabling/disabling timers based on Away-status
#
# if away on, enable all timers for scenes with names starting with "Away_" and
# disable all other scene timersif away off, disable all timers for scenes
# "Away_", and enable all other scene timers
#
# Author: moroen@gmail.com
#

import urllib2
import base64
import sys
import json

domoticzserver = "127.0.0.1:8080"
domoticzusername = ""
domoticzpassword = ""
awayDeviceName = "Away"
base64string = base64.encodestring('%s:%s' % (
    domoticzusername, domoticzpassword)).replace('\n', '')


def DomoticzRequest(url):
    request = urllib2.Request(url)
    request.add_header("Authorization", "Basic %s" % base64string)
    try:
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.URLError:
        print ("Error - Couldn't open URL")
        quit()


def DomoticzTimer(idx, status):
    if status:
        cmd = "enablescenetimer"
    else:
        cmd = "disablescenetimer"

    url = "http://" + domoticzserver + "/json.htm?type=command&param=" + \
        cmd + "&idx=" + str(idx)
    DomoticzRequest(url)


def setAway(away):
    url = "http://" + domoticzserver + "/json.htm?type=schedules&filter=scene"
    data = json.loads(DomoticzRequest(url))

    print (url)

    for k in data["result"]:
        # print str(k["TimerID"]) + ": " + k["DevName"]

        if k["DevName"].startswith("Away"):
            DomoticzTimer(k["TimerID"], away)
        else:
            DomoticzTimer(k["TimerID"], not(away))


if __name__ == "__main__":
    # Started as a standalone script

    if len(sys.argv) == 2:

        if sys.argv[1] == "on":
            status = True
        else:
            status = False

        setAway(status)
    else:
        print("away.py - requires exactly one argument (on/off)")
