local sourceDevice = '$Ute - Platting - Switch 1'
-- local sourceDevice = 'Test'


local monitorDevice = 'Stue 2 - Tak'
local groupOff = 'Group:Stue'
local sceneOn = 'Scene:Stue - Kveld'
local sceneDim = 'Scene:Stue - Dempet'

commandArray = {}
if (devicechanged[sourceDevice] == 'On') then
	print("Stue")
	print(monitorDevice..": "..otherdevices[monitorDevice].."|"..otherdevices_svalues[monitorDevice])

	if tonumber(otherdevices_svalues[monitorDevice]) > 45 and otherdevices[monitorDevice] ~= "Off" then
		commandArray[sceneDim]="On"
	elseif tonumber(otherdevices_svalues[monitorDevice]) <= 45 and otherdevices[monitorDevice] ~= "Off" then
		commandArray[groupOff] = "Off"
	elseif otherdevices[monitorDevice] == "Off" then
		commandArray[sceneOn] = "On"
	end
 	--if (otherdevices[targetDevice] == 'Off') then
	--	commandArray[targetDevice]='On'
	--else
	--	commandArray[targetDevice]='Off'
	--end

	-- commandArray[targetDevice]="Set Level 90"
end

return commandArray
