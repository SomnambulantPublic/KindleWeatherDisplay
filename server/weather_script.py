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
# 8 days with 6 data points
forecast = [[None]*6]*8
# constants help readability
dates = 0
icons = 1
lows = 2
highs = 3
briefs = 4
rains = 5

precis_xml = open('IDN11060.xml', 'rt')
precis_data = minidom.parse(precis_xml)
precis_areas = precis_data.getElementsByTagName('area')
for area in precis_areas:
    if area.getAttribute('description') == 'Gosford':
        periods = area.getElementsByTagName('forecast-period')
        for period in periods:
            forecast[periods.index(period)][dates] = period.getAttribute('start-time-local')
            elements = period.getElementsByTagName('*')
#        
#            # alternate to get element nodes wildcard above is to get all children
#            elements = period.childNodes 
#            # then trim out text nodes, text objects will fail .getAttribute()
#            # note: I don't mean element nodes with .tagName of text, these are fine
#            for i in range(elements.length):
#                if elements[i].nodeType == 3:
#                    elements.remove(elements[i])
#        
            for element in elements:
                if element.getAttribute('type') == 'forecast_icon_code':
                    forecast[periods.index(period)][icons] = int(element.firstChild.nodeValue)
                elif element.getAttribute('type') == 'air_temperature_minimum':
                    forecast[periods.index(period)][lows] = int(element.firstChild.nodeValue)
                elif element.getAttribute('type') == 'air_temperature_maximum':
                    forecast[periods.index(period)][highs] = int(element.firstChild.nodeValue)
                elif element.getAttribute('type') == 'precis':
                    forecast[periods.index(period)][briefs] = element.firstChild.nodeValue
                elif element.getAttribute('type') == 'probability_of_precipitation':
                    forecast[periods.index(period)][rains] = element.firstChild.nodeValue
                else:
                    continue
                
for i in range(8):
    for j in range(6):
        print(forecast[i][j])
                        
## TODO: try getChildren and nextSibling methods to clean up mess above (from below for period in periods)


# Enhance memory recovery
#dom.unprintlink()
