#!/usr/bin/python3

# Kindle Weather Display - Server-side script
# Chris Lovell, April 2018

# Updated for python3; and
# Parsing rewritten for Australian Government Bureau of Meteorology (BOM) data

# Based on the work of:
# Matthew Petroff (http://www.mpetroff.net/) September 2012

#### Notes: ####
#
# Commented-out code is for debug purposes
#
# BOM product descriptions: http://www.bom.gov.au/catalogue/anon-ftp.shtml
# Hosted: (browser) ftp://ftp.bom.gov.au/anon/gen/ or (client) ftp://ftp2.bom.gov.au
#
# #*1 - use of .getElementsByTagName('*') wildcard is to avoid use of .childNodes 
#       which would include non-element nodes needing to be excluded later (eg text-nodes)
#       (NB: text-nodes are NOT element-nodes with 'text' as a tagName)

from ftplib import FTP
from xml.dom import minidom
import datetime
import codecs

# constants
dates = 0
icons = 1
lows = 2
highs = 3
briefs = 4
rains = 5

# variable
xml_day_today = None
xml_day_today = None

# 'Array' of lists for data (8 days with 6 data points)
forecast = [[None for y in range(6)] for x in range(8)]

# Download weather data
bom = FTP('ftp2.bom.gov.au', user='anonymous', passwd='guest')
bom.cwd('/anon/gen/fwo')
precis_xml = open('IDN11060.xml', 'wt')
bom.retrlines('RETR IDN11060.xml', precis_xml.write)
precis_xml.close()
bom.quit()

# Parse weather data incl dates
precis_xml = open('IDN11060.xml', 'rt')
precis_data = minidom.parse(precis_xml)
precis_areas = precis_data.getElementsByTagName('area')
for area in precis_areas:
    if area.getAttribute('description') == 'Gosford':
        periods = area.getElementsByTagName('forecast-period')
        xml_date_today = periods[0].getAttribute('start-time-local').split('T', 1)[0]
        xml_day_today = datetime.datetime.strptime(xml_date_today, '%Y-%m-%d')
        for period in periods:
            pi = periods.index(period)
            forecast[pi][dates] = period.getAttribute('start-time-local')
            elements = period.getElementsByTagName('*') #*1 See Notes
            for element in elements:
                #print ("Period:" + str(pi))
                if element.getAttribute('type') == 'forecast_icon_code':
                    forecast[pi][icons] = str(element.firstChild.nodeValue)
                    #print ("Icon " + str(element.firstChild.nodeValue))
                    #print ("X: " + str(pi) + " , Y: " + str(icons))
                elif element.getAttribute('type') == 'air_temperature_minimum':
                    forecast[pi][lows] = str(element.firstChild.nodeValue)
                    #print ("Lows " + str(element.firstChild.nodeValue))
                    #print ("X: " + str(pi) + " , Y: " + str(lows))
                elif element.getAttribute('type') == 'air_temperature_maximum':
                    forecast[pi][highs] = str(element.firstChild.nodeValue)
                    #print ("Highs " + str(element.firstChild.nodeValue))
                    #print ("X: " + str(pi) + " , Y: " + str(highs))
                elif element.getAttribute('type') == 'precis':
                    forecast[pi][briefs] = element.firstChild.nodeValue
                    #print("Briefs " + str(element.firstChild.nodeValue))
                    #print ("X: " + str(pi) + " , Y: " + str(briefs))
                elif element.getAttribute('type') == 'probability_of_precipitation':
                    forecast[pi][rains] = element.firstChild.nodeValue
                    #print("Rains " + str(element.firstChild.nodeValue))
                    #print ("X: " + str(pi) + " , Y: " + str(rains))
            #print (forecast[pi])
            #print (forecast)


#for i in range(len(forecast)):
#    print ("i: " +str(i))
#    for j in range(len(forecast[i])):
#        print ("j: "+str(j))
#        print(forecast[i][j])
#    print(forecast[i])


#
# Preprocess SVG
#

# Open SVG to process
output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()

# Insert icons and temperatures
output = output.replace('ICON_ONE',str("ico"+forecast[0][1])).replace('ICON_TWO',str("ico"+forecast[1][1])).replace('ICON_THREE',str("ico"+forecast[2][1])).replace('ICON_FOUR',str("ico"+forecast[3][1]))
output = output.replace('HIGH_ONE',str(forecast[0][3])).replace('HIGH_TWO',str(forecast[1][3])).replace('HIGH_THREE',str(forecast[2][3])).replace('HIGH_FOUR',str(forecast[3][3]))
output = output.replace('LOW_ONE',str(forecast[0][2])).replace('LOW_TWO',str(forecast[1][2])).replace('LOW_THREE',str(forecast[2][2])).replace('LOW_FOUR',str(forecast[3][2]))

# Insert days of week
one_day = datetime.timedelta(days=1)
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
output = output.replace('DAY_THREE',days_of_week[(xml_day_today + 2*one_day).weekday()]).replace('DAY_FOUR',days_of_week[(xml_day_today + 3*one_day).weekday()])

# Write output
codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)





# Enhance memory recovery
#precis_data.unlink()

