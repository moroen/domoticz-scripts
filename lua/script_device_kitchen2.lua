local sourceDevice = '$Kjøkken - Switch 2'
local targetDevice = 'Kjøkken - Spot'

commandArray = {}

if (devicechanged[sourceDevice] == 'On') then
  print ("On: "..os.time())
  -- uservariables["clickTimer"] = string.format("d", os.time())
  commandArray['Variable:clickTimer'] = tostring(os.time())
elseif (devicechanged[sourceDevice] == 'Off') then
  local diff = os.difftime(os.time(), uservariables["clickTimer"])
  print ("Off")
  print ("clickTimer: "..uservariables["clickTimer"])
  print ("diffTime: "..diff)

  if (diff < 2) then
    if (otherdevices[targetDevice] == 'Off') then
  		commandArray[targetDevice]='On'
  	else
  		commandArray[targetDevice]='Off'
  	end
  else
    if tonumber(otherdevices_svalues[targetDevice]) >= uservariables[targetDevice..'_high'] then
      commandArray[targetDevice]='Set Level '..uservariables[targetDevice..'_low']
    else
      commandArray[targetDevice]='Set Level '..uservariables[targetDevice..'_high']
    end
  end
end

return commandArray
