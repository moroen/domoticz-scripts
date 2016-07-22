# -*- coding: utf-8 -*-

import domoticz
import udp as bc
import away as a
import time

import conditional_triggers as ctrig

domoticz.log("Python: triggerValue: ", domoticz.user_variables["conditional_trigger"])

triggers = {"$Kjøkken - Switch 1": "Kjøkken - Tak", "$Kjøkken - Switch 2": "Kjøkken - Spot"}

dev = domoticz.changed_device

if dev.name in triggers:
    targetDev = domoticz.devices[triggers[dev.name]]
    domoticz.log ("Python: Trigger: ", dev.name, " Target: ", targetDev.name)

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
            ctrig.toggleHighLow(targetDev)
        else:
            # Short click
            domoticz.log("Python: Trigger '", dev.name, "' short click performed")
            ctrig.toggle(targetDev)
            #ctrig.toggleHighLow(targetDev)

#
# if (changed_device_name == "Test"):
#     domoticz.log("Python: Device - Test changed")
#     domoticz.command(name="Test_Target", action="On", file=__file__)
