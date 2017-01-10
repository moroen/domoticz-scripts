# -*- coding: utf-8 -*-
import domoticz
import operator

operators = {"eg": operator.eq, "lt": operator.lt, "gt": operator.gt,
             "le": operator.le, "ge": operator.ge, "ne": operator.ne,
             "On": 1, "Off": 0}


def check_conditions(conditions):
    res = True

    for a in conditions:

        if "sensor" in a and "condition" in a:
            sensorDevice = domoticz.devices[a["sensor"]]
            # domoticz.log("Conditional scenes - sensor: ", sensorDevice.name, "s_value: ", sensorDevice.s_value, "n_value:", sensorDevice.n_value, "switch-type: ", sensorDevice.switch_type)

            if sensorDevice.switch_type == 0:
                # On/Off Switch - just check n_value
                res &= True if operators[a["condition"]] == sensorDevice.n_value else False
            elif sensorDevice.switch_type == 7:
                # MultiLevel
                if "condition" in a:
                    if a["condition"] == "On":
                        # N-value 1 (full on) or 2 (on, but dimmed)
                        res &= True if sensorDevice.n_value > 0 else False
                        #domoticz.log ("Condition On - n_value", sensorDevice.n_value, "res: ", res)
                    elif a["condition"] == "Off":
                        res &= True if sensorDevice.n_value == 0 else False
                        #domoticz.log ("Condition Off - n_value", sensorDevice.n_value, "res: ", res)
                    else:
                        res &= operators[a["condition"]](int(sensorDevice.s_value), int(a["val"]))
                else:
                    domoticz.log("Condtional scenes: Missing required key (condition)")
                    res = False
        else:
            domoticz.log("Conditional scenes: Missing required keys (sensor, condition)")
            res = False

    # domoticz.log("Conditional scenes - Condition: ", conditions, " res: ", res)
    return res

# Define triggers
# Due to using impulse-triggers, only execute scene when the trigger is Off

sceneTriggers = {"$Stue - Spot - Click":
                 [
                     {
                         "scene": "Stue - Dempet",
                         "conditions": [{"sensor": "Stue 2 - Tak", "condition": "ge", "val": 50},
                                        {"sensor": "Stue 2 - Tak", "condition": "On"}
                                        ]
                     },
                     {
                         "group": "Stue", "action": "Off",
                         "conditions": [{"sensor": "Stue 2 - Tak", "condition": "le", "val": 50}, {"sensor": "Stue 2 - Tak", "condition": "On"}]
                     },
                     {
                         "scene": "Stue - Kveld",
                         "conditions": [{"sensor": "Stue 2 - Tak", "condition": "Off"}]
                     }
                 ],
                 "$Gang - Trapp - SingleClick":
                     [
                         {
                             "scene": "Natt",
                             "conditions": [{"sensor": "Gang - Trapp", "condition": "On"}]
                         },
                         {
                             "scene": "Ettermiddag",
                             "conditions": [{"sensor": "Gang - Trapp", "condition": "Off"}]
                         }
                 ]
                 }


triggerDev = domoticz.changed_device

if triggerDev.name in sceneTriggers:
    currentTrigger = sceneTriggers[triggerDev.name]
    # domoticz.log("Conditional scenes: - ", triggerDev.name)
    for a in currentTrigger:
        if check_conditions(conditions=a["conditions"]):
            if "scene" in a:
                domoticz.log("Conditional scenes: Activating scene ", a["scene"])
                domoticz.command(name="Scene:" + a["scene"], action="On", file=__file__)
                break
            elif "group" in a:
                domoticz.log("Conditional scenes: Group ", a["group"], " ", a["action"])
                domoticz.command(name="Group:" + a["group"], action=a["action"], file=__file__)
                break
