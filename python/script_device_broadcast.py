import domoticz
import udp as bc

if 1:
    domoticz.log(
        "Python: Sending DeviceChange for device: ",
        changed_device_name)

    bc.send("Domoticz:DeviceChange:" + str(changed_device.id))
