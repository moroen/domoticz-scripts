# -*- coding: utf-8 -*-
import domoticz
import operator

operators = {"eg": operator.eq, "lt": operator.lt, "gt": operator.gt,
             "le": operator.le, "ge": operator.ge, "ne": operator.ne}


def check_conditions(s_value, conditions):
    res = True
    domoticz.log("Scenes - s_value: ", s_value)
    for a in conditions:
        # print s_value, a["opr"], a["val"]
        # print operators[a["opr"]](int(s_value), a["val"])
        res &= operators[a["opr"]](int(s_value), a["val"])

    return res

sceneTriggers = {"Test": [
    {"scene": "Test_Low", "sensor": "Stue - Hjørnelampe",
        "conditions": [{"opr": "gt", "val": 50}]},
    {"scene": "Test", "sensor": "Stue - Hjørnelampe",
     "conditions": [{"opr": "le", "val": 50}, {"opr": "lt", "val": 51}]}
]}

# print sceneTriggers

triggerDev = domoticz.changed_device

if triggerDev.name in sceneTriggers:
    currentTrigger = sceneTriggers[triggerDev.name]
    for a in currentTrigger:
        sensorDev = domoticz.devices[a["sensor"]]

        if check_conditions(s_value=sensorDev.s_value, conditions=a["conditions"]):
            domoticz.command(name="Scene:" + a["scene"], action="On", file=__file__)
