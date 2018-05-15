Kindle Weather Display
======================

## Weather Display Project for Amazon Kindle - Australia localised for Bureau of Meteorology data 

This project builds on scipts by Matthew Petroff's [Kindle Weather Display](https://mpetroff.net/2012/09/kindle-weather-display). Shell scripts are almost unchanged, but the python script was rewritten from the ground up for the data from BOM, using his original as a guide.

[Jennifer's 1347/365 Project](http://www.shatteredhaven.com/2012/11/1347365-kindle-weather-display.html) was also very helpful as it also built on Matthew's work and stepped through some parts.


Basics:  
A cron job on a Raspberry Pi or other device runs a bash shell script, which runs a python script that downloads weather data from the BOM, parses it and outputs it as find/replace into an svg. the bash script then calls other applications to convert it to a png and reduce its size, then places it into a lan-accessible web-server directory.  
On the kindle another cron job grabs the image and displays it. People suggest KUAL or KITE in order to run the initiation script (which sets up for the display by killing some processes), but just log in via ssh and run the scipt manually. 

You will need:  
* A Kindle  
* A server  
* Time

Skills you will need to implement this:  
* a little basic linux knowledge

Skills I learned re-implementing this:  
* Python scripting  
* xml file structure/parsing
* svg file structure/creation
* Inkscape  
* git
* nginx (super basics)
* John (the ripper)
* and built on linux knowledge of bash, bash scripting, ssh, cron

It took a large percentage of about 6-8 wks of my spare time.  
So take your time and use it as an opportunity to learn.  
I haven't yet even started to work on the wooden frame/enclosure for it to bring the whole project to a close
