after Jailbreak, there is no need to install Kite or KUAL 

to enable usbNetwork after dropping to file in usb drive mode type (on kinde)
;debugOn (return)
~usbNetwork

may like to change config:
default ssh server is dropbear, root pw is mario, framework pw is mario
may change to openSSH, pw for openSSH will be SN dependent, change while using dropbear (might work), or use SN/pw calculator online, or obtain passwd and shadow files and use John (the ripper)
may change to enable usbNetwork on boot, 
may change to enable ssh only on wifi, and keep usb to usb-drive mode

move files to kindle 
scp ./* root@<kindle.ip>:/mnt/us/weather/

login via ssh, 
mount fs as rw

ensure scripts executable 
chomd 777 ./*.sh

edit crontab manually
nano /etc/crontab/root

add following line, or similar (offset to allow server-script to run)
4,14,24,34,44,54 * * * * /mnt/us/weather/display-weather.sh

restart crond
/ect/init.d/cron restart

run init script to stop services and initiate display
./init-weather.sh

device will no longer respond to device keys, to turn off hold power button for ~20 seconds
