#!/usr/bin/python3

# Kindle Weather Display - Server-side script
# Chris Lovell, April 2018

# Updated for python3; and,
# Updated to use Australian Government Bureau of Meteorology (BOM) data
# Hosted: (browser) ftp://ftp.bom.gov.au/anon/gen/ or (client) ftp://ftp2.bom.gov.au
# Descriptions: http://www.bom.gov.au/catalogue/anon-ftp.shtml

# Inspired by the work of:
# Matthew Petroff (http://www.mpetroff.net/) September 2012

from ftplib import FTP
from xml.dom import minidom
import datetime
import codecs

#
# Download weather data
#
bom = FTP('ftp2.bom.gov.au', user='anonymous', passwd='guest')
bom.cwd('/anon/gen/fwo')
precis_xml = open('IDN11060.xml', 'wt')
bom.retrlines('RETR IDN11060.xml', precis_xml.write)
precis_xml.close()
bom.quit()
#
# Parse weather data
#
# 4 days with 6 data points
forecast = [[None]*6]*4
# constants help readability
dates = 0
icons = 1
highs = 2
lows = 3
briefs = 4
rains = 5

precis_xml = open('IDN11060.xml', 'rt')
precis_data = minidom.parse(precis_xml)
precis_areas = precis_data.getElementsByTagName('area')
for area in precis_areas:
    if area.getAttribute('description') == 'Gosford':
        periods = area.getElementsByTagName('forecast-period')
        # Get 4 days of forecast data
        for i in (0-3):
            forecast[i][dates] = periods[i].getAttribute('start-time-local')
            for period in periods:
                elements = period.getElementsByTagName('element')
                for element in elements:
                    if element.getAttribute('type') == 'forecast_icon_code':
                        forecast[i][icons] = int(element.firstChild.nodeValue)
                    elif element.getAttribute('type') == 'air_temperature_minimum':
                        forecast[i][lows] = int(element.firstChild.nodeValue)
                    elif element.getAttribute('type') == 'air_temperature_maximum':
                        forecast[i][highs] = int(element.firstChild.nodeValue)
                texts = period.getElementsByTagName('text')
                for text in texts:
                    if text.getAttribute('type') == 'precis':
                        forecast[i][briefs] = element.firstChild.nodeValue
                    elif text.getAttribute('type') == 'probability_of_precipitation':
                        forecast[i][rains] = element.firstChild.nodeValue
## TODO: try getChildren and nextSibling methods to clean up mess above (from below for period in periods)


# Enhance memory recovery
#dom.unlink()
