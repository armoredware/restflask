import uuid
import datetime
from common.database import Database
from common.utils import Utils
import models.users.errors as UserErrors
import re

__author__ = "mjd"

class Page(object):
    def __init__(self, 
                 domain, 
                 user_id, 
                 last_mod, 
                 timestamp,
                 url,
                 xss,
                 sqli,
                 sql,
                 csrf,
                 hash,
                 uptime,
                 loadspeed,
                 pagecontent,
                 externallinks,
                 scripts,
                 base64,
                 documenttype,
                 virus,
                 malware,
                 reputation,
                 popups,
                 bruteforce,
                 title,
                 redirect,
                 sensitivedata,
                 emailaddresses,
                 adaissues,
                 accesscontrol,
                 vulnerability,
                 scanned, _id=None ):
        self.domain= domain
        self.last_mod= last_mod
        self.timestamp= timestamp
        self.user_id= user_id
        self.url= url
        self.xss= xss
        self.sqli= sqli
        self.sql= sql
        self.csrf= csrf
        self.hash= hash
        self.uptime= uptime
        self.loadspeed= loadspeed
        self.pagecontent= pagecontent
        self.externallinks= externallinks
        self.scripts= scripts
        self.base64= base64
        self.documenttype= documenttype
        self.virus= virus
        self.malware= malware
        self.reputation= reputation
        self.popups= popups
        self.bruteforce= bruteforce
        self.title= title
        self.redirect= redirect
        self.sensitivedata= sensitivedata
        self.emailaddresses= emailaddresses
        self.adaissues= adaissues
        self.accesscontrol= accesscontrol
        self.vulnerability= vulnerability
        self.scanned= scanned
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='pages',
                        data=self.json())


    def update_to_mongo(self):
        Database.update(collection='pages', key= self.get_key(),
                        data=self.edited_json())

    def edited_json(self) :
        return { 
            '$set': { 'domain': self.domain, 
            'user_id': self.user_id, 
            'last_mod': self.last_mod, 
            'timestamp': self.timestamp,
            'url': self.url,
            'xss': self.xss,
            'sqli': self.sqli,
            'sql': self.sql,
            'csrf': self.csrf,
            'hash': self.hash,
            'uptime': self.uptime,
            'loadspeed': self.loadspeed,
            'pagecontent': self.pagecontent,
            'externallinks': self.externallinks,
            'scripts': self.scripts,
            'base64': self.base64,
            'documenttype': self.documenttype,
            'virus': self.virus,
            'malware': self.malware,
            'reputation': self.reputation,
            'popups': self.popups,
            'bruteforce': self.bruteforce,
            'title': self.title,
            'redirect': self.redirect,
            'sensitivedata': self.sensitivedata,
            'emailaddresses': self.emailaddresses,
            'adaissues': self.adaissues,
            'accesscontrol': self.accesscontrol,
            'vulnerability': self.vulnerability,
            'scanned': self.scanned } }

    def get_key(self):
        return { '_id': self._id }

    def json(self):
        return {
            'domain': self.domain, 
            'user_id': self.user_id, 
            'last_mod': self.last_mod, 
            'timestamp': self.timestamp,
            'url': self.url,
            'xss': self.xss,
            'sqli': self.sqli,
            'sql': self.sql,
            'csrf': self.csrf,
            'hash': self.hash,
            'uptime': self.uptime,
            'loadspeed': self.loadspeed,
            'pagecontent': self.pagecontent,
            'externallinks': self.externallinks,
            'scripts': self.scripts,
            'base64': self.base64,
            'documenttype': self.documenttype,
            'virus': self.virus,
            'malware': self.malware,
            'reputation': self.reputation,
            'popups': self.popups,
            'bruteforce': self.bruteforce,
            'title': self.title,
            'redirect': self.redirect,
            'sensitivedata': self.sensitivedata,
            'emailaddresses': self.emailaddresses,
            'adaissues': self.adaissues,
            'accesscontrol': self.accesscontrol,
            'vulnerability': self.vulnerability,
            'scanned': self.scanned,
            '_id': self._id 
            }

    @classmethod
    def from_mongo_domain(cls, page_url):
        #search_phrase ='.*'+re.escape(search_phrase)+'.*'
        #regex = re.compile(search_phrase,re.IGNORECASE)
        page_data = Database.find(collection='pages',
                                      query={'url': page_url }) #query={'description': {'$regex': '/n'}}
        return [cls(**page) for page in page_data]

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
            page_data = Database.find(collection='page',
                                      query={
                                      '$or':[
                                      {'name':{'$regex': regex, '$options': '' }},                                      
                                      {'page_info':{'$regex':regex, '$options': '' }},

                                      ]
                                      })#query={'description': {'$regex': '/n'}}
            if(search_type!="select"):
               page_data = Database.find(collection='pages',
                                      query={
                                      '$and':[
                                      {'name':{'$regex': regex, '$options': '' }},                                      
                                      #{'page_info':{'$regex':regex, '$options': '' }},
                                      {'page_type': search_type},
                                      ]
                                      })
        
        if(search_type !="select"):
            page_data = Database.find(collection='pages', query={'page_type': search_type})
        
        if(search_vintage !="select"):
            page_data = Database.find(collection='pages', query={'vintage': search_vintage})
        
        if(search_bottle !="select"):
            page_data = Database.find(collection='pages', query={'bottle_size': search_bottle})
            
        if(search_country !="select"):
            page_data = Database.find(collection='pages', query={'country': search_country})
        
        if(search_case !="select"):
            page_data = Database.find(collection='pages', query={'bottle_per_case': search_case})
        #else:
            #if (search_type=="select"|| search_vintage=="select"|| search_bottle="select"|| search_country=="select"|| search_case=="select")
            #page_data = Database.find(collection='pages',
                                          #query={'name': {'$regex': regex, '$options': '' } }) #query={'description': {'$regex': '/n'}}
                                          #query={
                                           #'$or': [
                                          #{'page_type': search_type},
                                          #{'vintage': search_vintage},
                                          #{'bottle_size': search_bottle},
                                          #{'country': search_country},
                                          #{'bottle_per_case': search_case},
                                          #]
                                          #})
        return [cls(**page) for page in page_data]

    @classmethod
    def from_mongo_id(cls, page_id):
        #search_phrase ='.*'+re.escape(search_phrase)+'.*'
        #regex = re.compile(search_phrase,re.IGNORECASE)
        page_data = Database.find(collection='pages',
                                      query={'_id': page_id }) #query={'description': {'$regex': '/n'}}
        return [cls(**page) for page in page_data]

    @classmethod
    def remove_from_mongo_id(cls, page_id):
        #search_phrase ='.*'+re.escape(search_phrase)+'.*'
        #regex = re.compile(search_phrase,re.IGNORECASE)
        page_data = Database.remove(collection='pages',
                                      query={'_id': page_id }) #query={'description': {'$regex': '/n'}}
        #return [cls(**page) for page in page_data]     
        return True

