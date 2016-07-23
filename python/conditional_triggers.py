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


def toggleHighLow(currentTrigger, targetDevice):
    targetLevel = int(targetDevice.s_value)
    action = ""

    if "Threshold" in currentTrigger:
        threshold = currentTrigger["Threshold"]
    else:
        threshold = currentTrigger["Low"]

    domoticz.log("Python: toggleHighLow - Target: ", targetDevice.name,
                 " n_value: ", targetDevice.n_value,
                 " s_value: ", targetDevice.s_value,
                 "Level: ", targetLevel,
                 "LowLevel: ", lowLevel,
                 "HighLevel: ", highLevel,
                 "Threshold: ", threshold
                 )

    if targetLevel <= int(threshold):
        action = "Set Level " + currentTrigger["High"]
    else:
        action = "Set Level " + currentTrigger["Low"]

    domoticz.log("Action:", action)
    domoticz.command(name=targetDevice.name, action=action, file=__file__)
