import uuid
import datetime
from common.database import Database
from common.utils import Utils
import models.users.errors as UserErrors
import re

__author__ = "mjd"

class Wine(object):
    def __init__(self, name, region, awards, winery,
                    bottle_size, bottle_per_case,
                    tasting_note, cs_price1, cs_price2,
                    cs_price3, bot_price1, bot_price2,
                    bot_price3, bottle_upcharge,
                    is_new, is_organic,
                    is_limited,
                    new_label, out_stock, wine_info,
                    country, appellation,
                    wine_type, variety, aging,
                    alcohol, img_url, vintage, _id=None ):
        self.region= region
        self.name= name
        self.awards = awards
        self.winery = winery
        self.bottle_size = bottle_size
        self.bottle_per_case = bottle_per_case
        self.vintage = vintage
        self.tasting_note = tasting_note
        self.cs_price1 = cs_price1
        self.cs_price2 = cs_price2
        self.cs_price3 = cs_price3
        self.bot_price1 = bot_price1
        self.bot_price2 = bot_price2
        self.bot_price3 = bot_price3
        self.bottle_upcharge = bottle_upcharge
        self.is_new = is_new
        self.is_organic = is_organic
        self.is_limited = is_limited
        self.new_label = new_label
        self.out_stock = out_stock
        self.wine_info = wine_info
        self.country = country
        self.appellation = appellation
        self.wine_type = wine_type
        self.variety = variety
        self.aging = aging
        self.alcohol = alcohol
        self.img_url = img_url
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='wines',
                        data=self.json())


    def update_to_mongo(self):
        Database.update(collection='wines', key= self.get_key(),
                        data=self.edited_json())

    def edited_json(self) :
        return { 
            '$set': { 'name': self.name,
            'region': self.region,
            'vintage': self.vintage,
            'awards': self.awards,
            'winery': self.winery,
            'bottle_size': self.bottle_size,
            'bottle_per_case': self.bottle_per_case,
            'tasting_note': self.tasting_note,
            'cs_price1': self.cs_price1,
            'cs_price2': self.cs_price2,
            'cs_price3': self.cs_price3,
            'bot_price1': self.bot_price1,
            'bot_price2': self.bot_price2,
            'bot_price3': self.bot_price3,
            'bottle_upcharge': self.bottle_upcharge,
            'is_new': self.is_new,
            'is_organic': self.is_organic,
            'is_limited': self.is_limited,
            'new_label': self.new_label,
            'out_stock': self.out_stock,
            'wine_info': self.wine_info,
            'country': self.country,
            'appellation': self.appellation,
            'wine_type': self.wine_type,
            'variety': self.variety,
            'aging': self.aging,
            'alcohol': self.alcohol,
            'img_url': self.img_url} } 

    def get_key(self):
        return { '_id': self._id }

    def json(self):
        return {
            'name': self.name,
            'region': self.region,
            'vintage': self.vintage,
            'awards': self.awards,
            'winery': self.winery,
            'bottle_size': self.bottle_size,
            'bottle_per_case': self.bottle_per_case,
            'tasting_note': self.tasting_note,
            'cs_price1': self.cs_price1,
            'cs_price2': self.cs_price2,
            'cs_price3': self.cs_price3,
            'bot_price1': self.bot_price1,
            'bot_price2': self.bot_price2,
            'bot_price3': self.bot_price3,
            'bottle_upcharge': self.bottle_upcharge,
            'is_new': self.is_new,
            'is_organic': self.is_organic,
            'is_limited': self.is_limited,
            'new_label': self.new_label,
            'out_stock': self.out_stock,
            'wine_info': self.wine_info,
            'country': self.country,
            'appellation': self.appellation,
            'wine_type': self.wine_type,
            'variety': self.variety,
            'aging': self.aging,
            'alcohol': self.alcohol,
            'img_url': self.img_url,
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
            wine_data = Database.find(collection='wines',
                                      query={
                                      '$or':[
                                      {'name':{'$regex': regex, '$options': '' }},                                      
                                      {'wine_info':{'$regex':regex, '$options': '' }},

                                      ]
                                      })#query={'description': {'$regex': '/n'}}
            if(search_type!="select"):
               wine_data = Database.find(collection='wines',
                                      query={
                                      '$and':[
                                      {'name':{'$regex': regex, '$options': '' }},                                      
                                      #{'wine_info':{'$regex':regex, '$options': '' }},
                                      {'wine_type': search_type},
                                      ]
                                      })
        
        if(search_type !="select"):
            wine_data = Database.find(collection='wines', query={'wine_type': search_type})
        
        if(search_vintage !="select"):
            wine_data = Database.find(collection='wines', query={'vintage': search_vintage})
        
        if(search_bottle !="select"):
            wine_data = Database.find(collection='wines', query={'bottle_size': search_bottle})
            
        if(search_country !="select"):
            wine_data = Database.find(collection='wines', query={'country': search_country})
        
        if(search_case !="select"):
            wine_data = Database.find(collection='wines', query={'bottle_per_case': search_case})
        #else:
            #if (search_type=="select"|| search_vintage=="select"|| search_bottle="select"|| search_country=="select"|| search_case=="select")
            #wine_data = Database.find(collection='wines',
                                          #query={'name': {'$regex': regex, '$options': '' } }) #query={'description': {'$regex': '/n'}}
                                          #query={
                                           #'$or': [
                                          #{'wine_type': search_type},
                                          #{'vintage': search_vintage},
                                          #{'bottle_size': search_bottle},
                                          #{'country': search_country},
                                          #{'bottle_per_case': search_case},
                                          #]
                                          #})
        return [cls(**wine) for wine in wine_data]

    @classmethod
    def from_mongo_id(cls, wine_id):
        #search_phrase ='.*'+re.escape(search_phrase)+'.*'
        #regex = re.compile(search_phrase,re.IGNORECASE)
        wine_data = Database.find(collection='wines',
                                      query={'_id': wine_id }) #query={'description': {'$regex': '/n'}}
        return [cls(**wine) for wine in wine_data]

    @classmethod
    def remove_from_mongo_id(cls, wine_id):
        #search_phrase ='.*'+re.escape(search_phrase)+'.*'
        #regex = re.compile(search_phrase,re.IGNORECASE)
        wine_data = Database.remove(collection='wines',
                                      query={'_id': wine_id }) #query={'description': {'$regex': '/n'}}
        #return [cls(**wine) for wine in wine_data]     
        return True
