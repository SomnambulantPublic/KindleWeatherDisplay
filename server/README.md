Server
======

## Raspberry Pi abbreviated instructions

install (sudo apt-get install ...)  
  * python3,  
  * librsvg2-bin (for rsvg-convert),  
  * pngcrush,  
  * nginx
  
change permissions for nginx web folder  
(chmod -R 777 /var/www/)

to run every 10 mins (offset for BOM data updates) install following line in crontab (crontab -e)  
3,13,23,33,43,53 * * * * /home/pi/weather/weather-script.sh

ensure scripts are executable  
chmod a+x weather-script.sh weather-script.py
