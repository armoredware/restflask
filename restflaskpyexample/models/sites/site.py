import uuid
import datetime
from common.database import Database
from common.utils import Utils
import models.users.errors as UserErrors
import re
import socket
import urllib2
#from time import time
import sys
import subprocess
import time

__author__ = "mjd"

class Site(object):
    def __init__(self, name, domain, user_id,
                 uptime,
                 alerts,
                 verbosity,
                 alias,
                 os,
                 middleware,
                 database,
                 platform,
                 cms,
                 appfirewall,
                 loadspeed,
                 vulnerabilities,
                 adacompliance,
                 virus,
                 malware,
                 pagerank,
                 backlinks,
                 ipaddress,
                 ports,
                 bruteforce,
                 traceroute,
                 price,
                 seal,
                 paid,
                 verified,
                 html,
                 js,
                 title,
                 thumbnail,
                 scanned,
                 resources, pages, timestamp, isLatest, _id=None ):
        self.name= name        
        self.domain= domain
        self.user_id= user_id
        self.uptime= uptime
        self.alerts = alerts
        self.verbosity = verbosity
        self.alias = alias
        self.os = os
        self.middleware = middleware
        self.database = database
        self.platform = platform
        self.cms = cms
        self.appfirewall = appfirewall
        self.loadspeed = loadspeed
        self.vulnerabilities = vulnerabilities
        self.adacompliance = adacompliance
        self.virus = virus
        self.malware = malware
        self.pagerank = pagerank
        self.backlinks = backlinks
        self.ipaddress = ipaddress
        self.ports = ports
        self.bruteforce = bruteforce
        self.traceroute = traceroute
        self.price = price
        self.seal = seal
        self.paid = paid
        self.verified = verified
        self.html = html
        self.js = js
        self.title = title
        self.thumbnail= thumbnail
        self.scanned = scanned
        self.resources = resources
        self.pages = pages
        self.timestamp = timestamp
        self.isLatest = isLatest
        self._id = uuid.uuid4().hex if _id is None else _id

    def scan_ip(self):
        domain = self.domain
        prep_domain=domain.replace("https://","")
        prep_domain=domain.replace("http://","")
        try:
            ipaddress= socket.gethostbyname(prep_domain)
        except: 
            ipaddress="unknown"
        Database.update(collection='sites', key= self.get_key(), data={'$set':{'ipaddress':ipaddress}})

    def scan_os(self):
        site_url = self.domain
        get_osInfo = subprocess.Popen(["python3.5","/var/www/py/armoredware.com/infosec/blackops/wig.py","-u",site_url],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
        get_osInfo.wait()
        osInfo = get_osInfo.communicate()[0]
        #get_osInfo.wait()
        return str(osInfo)

    def scan_speed(self):
        domain = self.domain
	loadspeed = ''
        try:
            stream = urllib2.urlopen(domain)
            start_time = time.time()
            output = stream.read()
            end_time = time.time()
            #time.sleep(10)
            stream.close()
            loadspeed= str(end_time-start_time)
        except:
            ipaddress="unknown"
        Database.update(collection='sites', key= self.get_key(), data={'$set':{'loadspeed':loadspeed}})



    def save_to_mongo(self):
        Database.insert(collection='sites',
                        data=self.json())


    def update_to_mongo(self):
        Database.update(collection='sites', key= self.get_key(),
                        data=self.edited_json())

    def edited_json(self) :
        return { 
            '$set': { 'name': self.name,
            'domain': self.domain,
            'user_id': self.user_id,
            'uptime': self.uptime,
            'alerts': self.alerts,
            'verbosity': self.verbosity,
            'alias': self.alias,
            'os': self.os,
            'middleware': self.middleware,
            'database': self.database,
            'platform': self.platform,
            'cms': self.cms,
            'appfirewall': self.appfirewall,
            'loadspeed': self.loadspeed,
            'vulnerabilities': self.vulnerabilities,
            'adacompliance': self.adacompliance,
            'virus': self.virus,
            'malware': self.malware,
            'pagerank': self.pagerank,
            'backlinks': self.backlinks,
            'ipaddress': self.ipaddress,
            'ports': self.ports,
            'bruteforce': self.bruteforce,
            'traceroute': self.traceroute,
            'price': self.price,
            'seal': self.seal,
            'paid': self.paid,
            'verified': self.verified,
            'html': self.html,
            'js': self.js,
            'title': self.title,
            'thumbnail': self.thumbnail,
            'scanned': self.scanned,
            'resources': self.resources,
            'pages': self.pages,
            'timestamp': self.timestamp,
            'isLatest': self.isLatest} }

    def get_key(self):
        return { '_id': self._id }

    def json(self):
        return {
            'name': self.name,
            'domain': self.domain,
            'user_id': self.user_id,
            'uptime': self.uptime,
            'alerts': self.alerts,
            'verbosity': self.verbosity,
            'alias': self.alias,
            'os': self.os,
            'middleware': self.middleware,
            'database': self.database,
            'platform': self.platform,
            'cms': self.cms,
            'appfirewall': self.appfirewall,
            'loadspeed': self.loadspeed,
            'vulnerabilities': self.vulnerabilities,
            'adacompliance': self.adacompliance,
            'virus': self.virus,
            'malware': self.malware,
            'pagerank': self.pagerank,
            'backlinks': self.backlinks,
            'ipaddress': self.ipaddress,
            'ports': self.ports,
            'bruteforce': self.bruteforce,
            'traceroute': self.traceroute,
            'price': self.price,
            'seal': self.seal,
            'paid': self.paid,
            'verified': self.verified,
            'html': self.html,
            'js': self.js,
            'title': self.title,
            'thumbnail': self.thumbnail,
            'scanned': self.scanned,
            'resources': self.resources,
            'pages': self.pages,
            'timestamp': self.timestamp,
            'isLatest': self.isLatest,
            '_id': self._id 
            }


    @classmethod
    def from_mongo(cls, search_phrase, search_type, search_vintage, search_bottle, search_country, search_case):
        #search_phraseC = search_phrase.title()
        #search_phrase1 = search_phrase
        #search_phrase2 = search_phrase.lower()
        search_phrase =".*"+re.escape(search_phrase)+".*"
        #search_phrase ='/'+re.escape(search_phrase)+'/i'
        regex = re.compile(search_phrase,re.IGNORECASE)
        search_type = search_type
        search_vintage = search_vintage
        search_bottle = search_bottle
        search_country = search_country
        search_case = search_case
        
        if (search_phrase!=""):
            site_data = Database.find(collection='sites',
                                      query={
                                      '$or':[
                                      {'name':{'$regex': regex, '$options': '' }},                                      
                                      {'site_info':{'$regex':regex, '$options': '' }},

                                      ]
                                      })#query={'description': {'$regex': '/n'}}
            if(search_type!="select"):
               site_data = Database.find(collection='sites',
                                      query={
                                      '$and':[
                                      {'name':{'$regex': regex, '$options': '' }},                                      
                                      #{'site_info':{'$regex':regex, '$options': '' }},
                                      {'site_type': search_type},
                                      ]
                                      })
        
        if(search_type !="select"):
            site_data = Database.find(collection='sites', query={'site_type': search_type})
        
        if(search_vintage !="select"):
            site_data = Database.find(collection='sites', query={'vintage': search_vintage})
        
        if(search_bottle !="select"):
            site_data = Database.find(collection='sites', query={'bottle_size': search_bottle})
            
        if(search_country !="select"):
            site_data = Database.find(collection='sites', query={'country': search_country})
        
        if(search_case !="select"):
            site_data = Database.find(collection='sites', query={'bottle_per_case': search_case})
        #else:
            #if (search_type=="select"|| search_vintage=="select"|| search_bottle="select"|| search_country=="select"|| search_case=="select")
            #site_data = Database.find(collection='sites',
                                          #query={'name': {'$regex': regex, '$options': '' } }) #query={'description': {'$regex': '/n'}}
                                          #query={
                                           #'$or': [
                                          #{'site_type': search_type},
                                          #{'vintage': search_vintage},
                                          #{'bottle_size': search_bottle},
                                          #{'country': search_country},
                                          #{'bottle_per_case': search_case},
                                          #]
                                          #})
        return [cls(**site) for site in site_data]

    @classmethod
    def from_mongo_id(cls, site_id):
        #search_phrase ='.*'+re.escape(search_phrase)+'.*'
        #regex = re.compile(search_phrase,re.IGNORECASE)
        site_data = Database.find(collection='sites',
                                      query={'_id': site_id }) #query={'description': {'$regex': '/n'}}
        return [cls(**site) for site in site_data]

    @classmethod
    def from_mongo_domain(cls, site_url):
        #search_phrase ='.*'+re.escape(search_phrase)+'.*'
        #regex = re.compile(search_phrase,re.IGNORECASE)
        site_data = Database.find(collection='sites',
                                      query={'domain': site_url }) #query={'description': {'$regex': '/n'}}
        return [cls(**site) for site in site_data]
    
    @staticmethod
    def site_exists(domain):
        site_data = Database.find_one("sites", {"domain": domain})  # Password in sha512 -> pbkdf2_sha512
        if site_data is None:
            return False
        else:
            return True

    @staticmethod
    def not_verified(domain):
        site_data = Database.find_one("sites", {"domain": domain, "verified": "false", "paid": "false"})  # Password $
        if site_data is None:
            return False
        else:
            return True

    @classmethod
    def remove_from_mongo_id(cls, site_id):
        #search_phrase ='.*'+re.escape(search_phrase)+'.*'
        #regex = re.compile(search_phrase,re.IGNORECASE)
        site_data = Database.remove(collection='sites',
                                      query={'_id': site_id }) #query={'description': {'$regex': '/n'}}
        #return [cls(**site) for site in site_data]     
        return True
