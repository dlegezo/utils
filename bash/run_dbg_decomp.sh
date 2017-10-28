MALWARE_DIR="F:\\"
ATTACK_PATH="$MALWARE_DIR$1\\"
FULL_PATH="$ATTACK_PATH$2"

# echo $FULL_PATH
if [ $3 == "dbg" ]; then
	vboxmanage startvm <VM32ID_here>
	vboxmanage guestcontrol <VM32ID_here> --username <UNAME_here> run --exe "C:\0_Tools\ollydbg\OllyDbg.exe" -- OllyDbg.exe/arg0 $FULL_PATH &
elif [ $3 == "dbg64" ]; then
	vboxmanage startvm <VM64ID_here>	
	vboxmanage guestcontrol <VM64ID_here> --username <UNAME_here> run --exe "F:\0_tools\x64dbg\release\x64\x64dbg.exe" -- x64dbg.exe/arg0 $FULL_PATH &
elif [ $3 == "apk" ]; then
	vboxmanage startvm <VMAPKID_here>
	vboxmanage guestcontrol <VMAPKID_here> --username <UNAME_here> run --exe "F:\0_tools\JEB_1.5\jeb_wincon.bat" -- jeb_wincon.bat/arg0 $FULL_PATH &
elif [ $3 == "adb" ]; then
	vboxmanage startvm <VMAPKID_here>
	adb connect <VMIP>
	echo $FULL_PATH
	adb install $FULL_PATH
fi
