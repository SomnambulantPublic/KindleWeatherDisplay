Kindle Weather Display
======================

## Weather Display Project for Amazon Kindle - Australia localised for Bureau of Meteorology data 

This project builds on scipts by [Matthew Petroff's Kindle Weather Display](https://mpetroff.net/2012/09/kindle-weather-display). Shell scripts are almost unchanged, but the python script was rewritten from the ground up for the data from BOM, using his original as a guide.

[Jennifer's 1347/365 Project](http://www.shatteredhaven.com/2012/11/1347365-kindle-weather-display.html) was also very helpful as it also built on Matthew's work and stepped through some parts.

However both project logs suggest installing KUAL or KITE in order to run the initiation script (which sets up for the display by killing some services), but I reccoment just logging in via ssh and running the scipt manually. 


Overview:  
A cron job on a Raspberry Pi or other device runs a bash shell script, which calls a python script which downloads weather data from the BOM, parses it and outputs it as find/replace into a preprepared svg image. The bash script then calls two other applications to convert it to a png, and reduce its size, then places it into a web-server directory.  
On the kindle another cron job grabs the image over wifi and displays it. 

You will need:  
* A Kindle (I used a Kindle 4 which has a 600x800 px display)  
* A server (I used a Raspberry Pi Model B Gen 1)  
* Time to localise to your location and modify if you wish

Skills you will need to implement this as-is:  
* a little basic linux knowledge

Skills I learned re-implementing this:  
* Python scripting  
* xml file structure/parsing  
* svg file structure/creation  
* Inkscape  
* git  
* nginx (super basics)  
* John (the ripper)  
* and built on linux knowledge of bash, bash scripting, ssh, cron, etc

It took a large percentage of my spare time for about 6-8 wks.  
So take your time and use it as an opportunity to learn.  
I have yet to start work on the wooden frame/enclosure for it to bring the whole project to a close.

There are other README files, with useful information you might like to read
