import time
import os
import urllib2
import subprocess
from models.sites.site import Site


def init_scan(site_url):
	site= Site.from_mongo_domain(site_url)
	site[0].scan_speed
	subprocess.Popen(["python3.5","/var/www/py/armoredware.com/infosec/blackops/wig.py","-u",site_url,"&"],stdout = subprocess.PIPE,stderr = subprocess.PIPE, shell = True)
	get_osInfo.wait()
	time.sleep(60)
	osInfo = get_osInfo.communicate()[0]
	get_osInfo.wait()
	#update last scan time


while True:
	open DB
	create list of sites verified
	for site in site_list: 
		init_scan(site)	
	time.sleep(60000)


	
