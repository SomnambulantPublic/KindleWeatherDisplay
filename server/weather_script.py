#!/usr/bin/python3

# Kindle Weather Display - Server-side script
# Chris Lovell, April 2018

# Updated for python3;
# Parsing rewritten for Australian Government Bureau of Meteorology (BOM) data;
# Additional data elements added to output

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
from datetime import datetime, timedelta


# Constants
dates = 0
icons = 1
lows = 2
highs = 3
briefs = 4
rains = 5

apparent = 0
actual = 1
humid = 2
winddir = 3
windkmh = 4
windkts = 5

# Strings
xml_date_today = None
parse_descript = ""

# Objects
xml_day_today = None
obs_ID = None
forecast_ID = None
img_ID = datetime.now()

# Arrays for data 
# precis forecast (8 days with 6 data points)
forecast = [["" for y in range(6)] for x in range(8)]
# descriptive forecast (8 days)
descript = ["" for z in range(8)]
# current conditions
observations = ["" for v in range(6)]


# Download weather forecast
bom = FTP('ftp2.bom.gov.au', user='anonymous', passwd='guest')
bom.cwd('/anon/gen/fwo')
precis_xml = open('IDN11052.xml', 'wt')
bom.retrlines('RETR IDN11052.xml', precis_xml.write)
precis_xml.close()
bom.quit()


# Parse weather data incl issue date time, forecast dates, precis descriptions, icons
precis_xml = open('IDN11052.xml', 'rt')
precis_data = minidom.parse(precis_xml)
precis_areas = precis_data.getElementsByTagName('area')
forecast_ID = datetime.strptime(precis_data.getElementsByTagName('issue-time-local')[0].firstChild.nodeValue, '%Y-%m-%dT%H:%M:%S+10:00')
for area in precis_areas:
    if area.getAttribute('description') == 'Gosford':
        periods = area.getElementsByTagName('forecast-period')
        xml_date_today = periods[0].getAttribute('start-time-local').split('T', 1)[0]
        xml_day_today = datetime.strptime(xml_date_today, '%Y-%m-%d')
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
                    forecast[pi][briefs] = str(element.firstChild.nodeValue)
                    #print("Briefs " + str(element.firstChild.nodeValue))
                    #print ("X: " + str(pi) + " , Y: " + str(briefs))
                elif element.getAttribute('type') == 'probability_of_precipitation':
                    forecast[pi][rains] = str(element.firstChild.nodeValue)
                    #print("Rains " + str(element.firstChild.nodeValue))
                    #print ("X: " + str(pi) + " , Y: " + str(rains))
            #print (forecast[pi])
            #print (forecast)
    # Get all descriptive forecasts
    if area.getAttribute('description') == 'Central Coast':
        periods = area.getElementsByTagName('forecast-period')
        for period in periods:
            pi = periods.index(period)
            elements = period.getElementsByTagName('*') #*1 See Notes
            for element in elements:
                #print ("Period:" + str(pi))
                if element.getAttribute('type') == 'forecast':
                    descript[pi] = str(element.firstChild.nodeValue) 
precis_xml.close()

#for i in range(len(forecast)):
#    print ("i: " +str(i))
#    for j in range(len(forecast[i])):
#        print ("j: "+str(j))
#        print(forecast[i][j])
#    print(forecast[i])


# Split long forecast (for today only) into multiple lines, also rudimentary text-wrap, and format for SVG text
for w in range(len(descript[0].split('. '))):
    split_descript = str(descript[0][:-1].split('. ')[w])
    if len(split_descript) > 55:
        n = split_descript.index(' ', 45)
        parse_descript = parse_descript + """<tspan dy="22" x="300">""" + split_descript[:n] + "</tspan>" + """<tspan dy="22" x="300">""" + split_descript[(n+1):] + "</tspan>"
    else:
        parse_descript = parse_descript + """<tspan dy="22" x="300">""" + split_descript + "</tspan>"
        
# Split precis for rudimentary text-wrap, and format for SVG text
for u in range(len(forecast)):
    # List containing x coordinates for displaying precis data
    k = [0,100,300,500,0,0,0,0]
    # Remove trailing period '.'    
    precis = forecast[u][briefs][:-1]
    # If longer than 21 characters, find next space after character position 12, then manually split at that point
    if len(precis) > 21:
        n = precis.index(' ', 12)
        forecast[u][briefs] = '<tspan dy="17" x="' + str(k[u]) + '">' + precis[:n] + "</tspan>" + '<tspan dy="17" x="' + str(k[u]) + '">' + precis[(n+1):] + "</tspan>"
    else:
        forecast[u][briefs] = '<tspan dy="17" x="' + str(k[u]) + '">' + precis + "</tspan>"    

# Download observations
bom = FTP('ftp2.bom.gov.au', user='anonymous', passwd='guest')
bom.cwd('/anon/gen/fwo')
obs_xml = open('IDN60920.xml', 'wt')
bom.retrlines('RETR IDN60920.xml', obs_xml.write)
obs_xml.close()
bom.quit()

# Parse weather observations
obs_xml = open('IDN60920.xml', 'rt')
obs_data = minidom.parse(obs_xml)
obs_ID = datetime.strptime(obs_data.getElementsByTagName('issue-time-local')[0].firstChild.nodeValue, '%Y-%m-%dT%H:%M:%S+10:00')
obs_stations = obs_data.getElementsByTagName('station')
for station in obs_stations:
    if station.getAttribute('description') == 'Gosford':
        elements = station.getElementsByTagName('*')
        for element in elements:
            element_type_attrib = element.getAttribute('type')
            if element_type_attrib == 'apparent_temp':
                observations[apparent] = str(element.firstChild.nodeValue)
            elif element_type_attrib == 'air_temperature':
                observations[actual] = str(element.firstChild.nodeValue)
            elif element_type_attrib == 'rel-humidity':
                observations[humid] = str(element.firstChild.nodeValue)
            elif element_type_attrib == 'wind_dir_deg':
                observations[winddir] = int(element.firstChild.nodeValue)
            elif element_type_attrib == 'wind_spd_kmh':
                observations[windkmh] = int(element.firstChild.nodeValue)
            elif element_type_attrib == 'wind_spd':
                observations[windkts] = str(element.firstChild.nodeValue)
obs_xml.close()


# TODO consider UV
# TODO consider sunrise and sunset



# Load from preprocess SVG and substitute values

# Open SVG to process
output = open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()

# Insert icons
output = output.replace('ICON_ZERO',str("ico"+forecast[0][icons])).replace('ICON_ONE',str("ico"+forecast[1][icons])).replace('ICON_TWO',str("ico"+forecast[2][icons])).replace('ICON_THREE',str("ico"+forecast[3][icons]))

# Insert temperatures
output = output.replace('HIGH_ZERO',forecast[0][highs]).replace('HIGH_ONE',forecast[1][highs]).replace('HIGH_TWO',forecast[2][highs]).replace('HIGH_THREE',forecast[3][highs])
output = output.replace('LOW_ZERO',forecast[0][lows]).replace('LOW_ONE',forecast[1][lows]).replace('LOW_TWO',forecast[2][lows]).replace('LOW_THREE',forecast[3][lows])

# Insert precis
output = output.replace('PRECIS_ONE',forecast[1][briefs]).replace('PRECIS_TWO',forecast[2][briefs]).replace('PRECIS_THREE',forecast[3][briefs])

# Insert descript
output = output.replace('DESCRIPT_ZERO',parse_descript)

# Insert days of week words
one_day = timedelta(days=1)
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
output = output.replace('DAY_TWO',days_of_week[(xml_day_today + 2*one_day).weekday()]).replace('DAY_THREE',days_of_week[(xml_day_today + 3*one_day).weekday()])

# Insert current observations
# feels like, actual temp, humidity, 
output = output.replace('FEELS_NOW',observations[apparent]).replace('TEMP_NOW',observations[actual]).replace('HUMID_NOW',observations[humid])

# Insert wind direction, pointer visibility, speedkmh, speedkts
output = output.replace('WIND_DEG',str(observations[winddir]+180)).replace('WIND_KTS',observations[windkts]).replace('WIND_KMH',str(observations[windkmh]))
if observations[windkmh] > 0:
    output = output.replace('POINTER_VIS','visible')
else:
    output = output.replace('POINTER_VIS','hidden')

# Insert timestamps
output = output.replace('IMG_GEN_DT',img_ID.strftime('%Y-%m-%d %H:%M:%S')).replace('FORECAST_DT',forecast_ID.strftime('%Y-%m-%d %H:%M:%S')).replace('OBS_DT',obs_ID.strftime('%Y-%m-%d %H:%M:%S'))

# Write output
open('weather-script-output.svg', 'w', encoding='utf-8').write(output)

# Enhance memory recovery
precis_data.unlink()
obs_data.unlink()
