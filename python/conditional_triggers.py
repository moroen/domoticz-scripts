# -*- coding: utf-8 -*-

import domoticz

import reloader
reloader.auto_reload(__name__)

longClickDuration = 2
triggerOnTime = {}

def toggle(targetDevice):

    domoticz.log("Python: Toggle - ", targetDevice.name)

    if targetDevice.n_value == 0:
        domoticz.command(name=targetDevice.name, action="On", file=__file__)
    else:
        domoticz.command(name=targetDevice.name, action="Off", file=__file__)
    return None


def toggleHighLow(targetDevice, lowLevel=50, highLevel=100):
    targetLevel = int(targetDevice.s_value)
    domoticz.log("Python: toggleHighLow - Target: ", targetDevice.name, " n_value: ", targetDevice.n_value, " s_value: ", targetDevice.s_value, "Level: ", targetLevel)

    if targetLevel < highLevel:
        domoticz.command(name=targetDevice.name, action="Set Level "+str(highLevel), file=__file__)
    else:
        domoticz.command(name=targetDevice.name, action="Set Level "+str(lowLevel), file=__file__)
