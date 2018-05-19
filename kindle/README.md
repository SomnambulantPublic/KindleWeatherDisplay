Kindle
======

Jailbreaking your Kindle is ridiculously simple, please follow the instructions for the Jailbreak itelf, getting usbNetwork installed, and configuring ssh-over-usb available here:  
[https://wiki.mobileread.com/wiki/Kindle4NTHacking](https://wiki.mobileread.com/wiki/Kindle4NTHacking)  
useful files available here:  
[https://www.mobileread.com/forums/showthread.php?t=88004](https://www.mobileread.com/forums/showthread.php?t=88004) 

Regarding the Jailbreak and usbNetwork, read the README's there too!

After Jailbreaking, there is no need to install Kite or KUAL (see other README in project root directory)

Regarding SSH and usbNetwork configuration:  
The default ssh server is Dropbear. While using Dropbear, the 'root' pw is 'mario'; 'framework' pw is 'mario'  
You may change the server to OpenSSH. Then the pw for 'root' for will be Serial Number dependent. You could try:  
* to change the root pw while using dropbear (this might work); or,  
* use a SN/pw calculator online [https://www.sven.de/kindle/](https://www.sven.de/kindle/)  
Alternatively do it the hard way and obtain the 'passwd' and 'shadow' files (while using Dropbear) and use John (the ripper) to brute force them  
You may decide to change to enable usbNetwork on boot (I did)  
You may decide to change to enable ssh only on wifi, and keep usb to usb-drive mode (I did)

When you are ready to install your scripts on your Kindle
move files to kindle via scp/ssh or via usb-drive mode. I chose /mnt/us/weather/ (where /mnt/us/ is the root folder you see in usb-drive mode)

Then login via ssh;  
Mount the filesystem as rw;  
Ensure scripts executable;  

Then edit the crontab manually  
eg: $ nano /etc/crontab/root

add following line, or similar (will run every 10 minutes, times are offset to allow server-script to run):  
4,14,24,34,44,54 * * * * /mnt/us/weather/display-weather.sh

restart crond  
eg: $ /ect/init.d/cron restart

run initialisation script to stop services and run the display script the first time  
/mnt/us/weather/init-weather.sh

The device will no longer respond to device keys, to turn off hold power button for ~20 seconds  

After powering back on again it will appear to behave normally at first. I have experience occasions I have yet to fully quatify, but it appears the cron job will continue to run, so every 10 mins it will fetch and display the weather. It WILL respond to device keys in this state (as you have not run the initialisation script) so you can simply page-turn to resume reading.  
This has also occured in screensaver mode (idle time-out; or short-press power button), but obviously won't respond to device keys until you press the power button.  
Even when the Kindle appears off (long-press power button - screen is cleared) the cron job has run. But in a power-down mode wifi is disabled, so it will display the weather error message.  
The initialisation script disables the service that puts the kindle to sleep after inactivty, and the one which supports normal reader functionality.  
To resume default Kindle operation, remove the line added to the crontab (above) and restart crond.
