# -*- coding: utf-8 -*-
import domoticz
import operator

operators = {"eg": operator.eq, "lt": operator.lt, "gt": operator.gt,
             "le": operator.le, "ge": operator.ge, "ne": operator.ne,
             "On": 1, "Off": 0}


def check_conditions(conditions):
    res = True

    for a in conditions:
        # print s_value, a["opr"], a["val"]
        # print operators[a["opr"]](int(s_value), a["val"])
        sensorDevice = domoticz.devices[a["sensor"]]
        domoticz.log("Scenes - sensor: ", sensorDevice.name, "switch_type: ", sensorDevice.switch_type, "n_value: ", sensorDevice.n_value, " s_value: ", sensorDevice.s_value)

        if sensorDevice.switch_type == 0:
            # On/Off Switch
            res &= True if operators[a["val"]] == sensorDevice.n_value else False
            domoticz.log("On/Off: ", a, res)

        elif sensorDevice.switch_type == 7:
            # MultiLevel
            res &= operators[a["opr"]](int(sensorDevice.s_value), int(a["val"]))
            domoticz.log("Multilevel: ", a, res)

    return res

sceneTriggers = {"Test": [
    {"scene": "Test_Low",
        "conditions": [{"sensor": "Test", "val": "Off"}, {"sensor": "Stue - Hjørnelampe", "opr": "gt", "val": 50}]},
    {"scene": "Test",
        "conditions": [{"sensor": "Test", "val": "Off"}, {"sensor": "Stue - Hjørnelampe", "opr": "le", "val": 50}]}
]}

# print sceneTriggers

triggerDev = domoticz.changed_device

if triggerDev.name in sceneTriggers:
    currentTrigger = sceneTriggers[triggerDev.name]
    for a in currentTrigger:

        if check_conditions(conditions=a["conditions"]):
            # domoticz.command(name="Scene:" + a["scene"], action="On", file=__file__)
            domoticz.log("Tjoho!")
