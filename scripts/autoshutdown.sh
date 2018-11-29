#!/bin/bash

CHECK_TIME=300		# Check cpu load every CHECK_TIME [s]
CPU_THRESHOLD=0.02	# Average CPU threshold [%] 

# Run the script in /etc/rc.local 
# (before last line `exit 0` to run it on startup) with training & to run in backgroud
# `absolute_path_dir/autoshutdown.sh &`
#
# If  /etc/rc.local doesn't exists  (Ubuntu 18.04) use
# > printf '%s\n' '#!/bin/bash' 'exit 0' | sudo tee -a /etc/rc.local
# > sudo chmod +x /etc/rc.local
# Edit /etc/rc.local
# > sudo reboot

# Check if running as root, otherwise shutdown doesn't work
if [[ $EUID > 0 ]]
  then echo "Please run as root or sudo"
  exit
fi

sleep $CHECK_TIME
while true #runs forever
do
	a=`cut -d ' ' -f 3 /proc/loadavg` #set a = load avg.
	if [ $(echo "$a < $CPU_THRESHOLD" | bc) -ne 0 ]; then #If load avg. is less than threshold
		echo "Shutting down; avg workload=$a < $CPU_THRESHOLD for last 15 minutes"
		shutdown
		sleep 120  # In case user cancel, script should continue
	else #If it's greater than threshold
		# echo "Working $a"
		:
	fi
	sleep $CHECK_TIME #Wait and try again
			
done
