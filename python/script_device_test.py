# -*- coding: utf-8 -*-

import domoticz
import udp as bc
import away as a


def toggle(device_name):
    dev = domoticz.devices[device_name]
    domoticz.log("Python: Toggle - ", dev.name)

    domoticz.log("Python: Toggle current s_value: ", dev.s_value, " n_value: ", dev.n_value)
    if dev.n_value == 0:
        domoticz.command(name=device_name, action="On", file=__file__)
    else:
        domoticz.command(name=device_name, action="Off", file=__file__)
    return None

if 0:
    domoticz.log("Python: Device", changed_device_name)
    bc.send("Domoticz:DeviceChange:" + str(changed_device.id))


if domoticz.changed_device_name == "Test":
    toggle(device_name="Test_Target")
#
# if (changed_device_name == "Test"):
#     domoticz.log("Python: Device - Test changed")
#     domoticz.command(name="Test_Target", action="On", file=__file__)
