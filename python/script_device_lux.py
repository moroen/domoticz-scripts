import DomoticzEvents as DE

from datetime import datetime, time

def in_between(now, strStart, strEnd):

    strStart=strStart.split(":")
    strEnd=strEnd.split(":")
    start=time(int(strStart[0]), int(strStart[1]))
    end=time(int(strEnd[0]), int(strEnd[1]))

    if start <= end:
        return start <= now < end
    else: # over midnight e.g., 23:30-04:15
        return start <= now or now < end


trigger = "Ute - Lux"

targets = [
    {"target": "Test A", "threshold": 500, "start": "07:00", "end": "23:00"},
    {"target": "Test B", "threshold": 700, "start": "07:00", "end": "23:00"}
]

if DE.changed_device_name == trigger:
    s_val = DE.changed_device.s_value

    for aTarget in targets:
        if in_between(datetime.now().time(), aTarget["start"], aTarget["end"]):

            targetDevice = DE.Devices[aTarget["target"]]
    
            DE.Log(targetDevice.Describe())
            # DE.Log(targetDevice.name)

            if int(s_val) < 500:
                if targetDevice.n_value == 0:
                    DE.Command(targetDevice.name, "On")
            else:
                if targetDevice.n_value == 1:
                    DE.Command(targetDevice.name, "Off")


    