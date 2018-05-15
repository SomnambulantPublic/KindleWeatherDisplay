<h1>Server</h1>

<h2>Raspberry Pi abbreviated instructions</h2>

<p>install (sudo apt-get install ...)  
<ul>
  <li>python3,</li>
  <li>librsvg2-bin (for rsvg-convert),</li>
  <li>pngcrush,</li>
  <li>nginx</li>
</ul></p>

<p>change permissions for nginx web folder  
(chmod -R 777 /var/www/)</p>

<p>to run every 10 mins (offset for BOM data updates) install following line in crontab (crontab -e)  
  3,13,23,33,43,53 * * * * /home/pi/weather/weather-script.sh</p>

<p>ensure scripts are executable  
chmod a+x weather-script.sh weather-script.py</p>
