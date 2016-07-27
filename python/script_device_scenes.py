# -*- coding: utf-8 -*-
import domoticz
import operator

operators = {"eg": operator.eq, "lt": operator.lt, "gt": operator.gt,
             "le": operator.le, "ge": operator.ge, "ne": operator.ne,
             "On": 1, "Off": 0}


def check_conditions(conditions):
    res = True

    for a in conditions:
        if "sensor" in a and "val" in a:
            sensorDevice = domoticz.devices[a["sensor"]]

            domoticz.log("Conditional scenes: sensor: ", sensorDevice.name, "s_value: ", sensorDevice.s_value, "n_value:", sensorDevice.n_value)

            if sensorDevice.switch_type == 0:
                # On/Off Switch
                res &= True if operators[a["val"]] == sensorDevice.n_value else False
            elif sensorDevice.switch_type == 7:
                # MultiLevel
                if "opr" in a:
                    res &= operators[a["opr"]](int(sensorDevice.s_value), int(a["val"]))
                else:
                    domoticz.log("Condtional scenes: Missing required key (opr)")
                    res = False
        else:
            domoticz.log("Conditional scenes: Missing required keys (sensor, val)")
            res = False

    return res

# Define triggers
# Due to using impulse-triggers, only execute scene when the trigger is Off

sceneTriggers = {"$Ute - Platting - Switch 1": [
    {"scene": "Stue - Dempet",
        "conditions": [{"sensor": "$Ute - Platting - Switch 1", "val": "Off"}, {"sensor": "Stue 2 - Tak", "opr": "ge", "val": 50}]},
    {"scene": "Stue - Av",
        "conditions": [{"sensor": "$Ute - Platting - Switch 1", "val": "Off"}, {"sensor": "Stue 2 - Tak", "opr": "le", "val": 50}]}
]}

print sceneTriggers

triggerDev = domoticz.changed_device

if triggerDev.name in sceneTriggers:
    currentTrigger = sceneTriggers[triggerDev.name]
    for a in currentTrigger:

        if check_conditions(conditions=a["conditions"]):
            domoticz.command(name="Scene:" + a["scene"], action="On", file=__file__)
