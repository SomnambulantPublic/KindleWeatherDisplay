Server
======

## Raspberry Pi abbreviated instructions

install:  
  * python3;
  * librsvg2-bin (for rsvg-convert);  
  * pngcrush;  
  * nginx.
  
Change permissions for nginx web folder (/var/www/) so scripts that are run as non-root users can add files (I'll let you determine if this is a security issue for you. I disabled the root account on my RPi, as a result root's crontab doesn't work, so this is my solution - suggestions??)  

Place the scripts on the server.  
I chose /home/pi/weather/

ensure scripts are executable (needed for shell script; perhaps not for the python script, as we call it as a argument to calling python3 - ???)

To run every 10 mins (offset for BOM data updates) install following line in crontab  
3,13,23,33,43,53 * * * * /home/pi/weather/weather-script.sh

## Note  
* There are a number of data points saved into variables in the python script that aren't used anywhere, you may decide to use them.
* There are a number of icons missing (eg snow,cyclone) and extra (eg sunrise,sunset) in the preprocess svg, you may decide to add them or use ones not in use
