# -*- coding: utf-8 -*-

import domoticz
import time

import conditional_triggers as ctrig

# Dict format: Trigger: Settings
# Settings:
#   Required parameters:
#       Target: Name of actuator (dimmer)
#       High: Level when switched to High (0-100)
#       Low: Level when switched to low (0-100)
#   Optional parameters:
#       Threshold:  if current level less or equal to threhold, dimmer set to high
#                   if current level more than threshold, dimmer set to low
#                   default = lowLevel

triggers = {
            "$Kjøkken - Switch 1": {"Target": "Kjøkken - Tak", "High": "100", "Low": "50"},
            "$Kjøkken - Switch 2": {"Target": "Kjøkken - Spot", "High": "100", "Low": "35"}
            }

# Changed device
dev = domoticz.changed_device

if dev.name in triggers:
    currentTrigger = triggers[dev.name]
    targetDev = domoticz.devices[currentTrigger["Target"]]
    domoticz.log("Python: Trigger: ", dev.name, " Target: ", targetDev.name)

    if dev.n_value == 1:
        ctrig.triggerOnTime[dev.name] = time.time()
        domoticz.log("Python: Trigger '", dev.name, "' on: ", ctrig.triggerOnTime[dev.name])
    if dev.n_value == 0:
        offTime = time.time()
        delta = offTime - ctrig.triggerOnTime[dev.name]
        domoticz.log("Python: Trigger '", dev.name, "' off: ", offTime, "delta: ", delta)

        if delta >= ctrig.longClickDuration:
            # Long click
            domoticz.log("Python: Trigger '", dev.name, "' long click performed")
            ctrig.toggleHighLow(currentTrigger, targetDev)
        else:
            # Short click
            domoticz.log("Python: Trigger '", dev.name, "' short click performed")
            ctrig.toggle(targetDev)
            # ctrig.toggleHighLow(targetDev)
