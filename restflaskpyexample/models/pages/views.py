from flask import Blueprint, request, session, url_for, render_template, jsonify
from werkzeug.utils import redirect
from models.pages.page import Page
#import models.pages.errors as PageErrors
#import models.users.decorators as user_decorators
from flask_jwt import jwt_required, current_identity
#import subprocess
#import urllib2
#import telnetlib
#import time

__author__ = 'mjd'

page_blueprint = Blueprint('pages', __name__)

@page_blueprint.route('/page_search')
def page_search():
    return jsonify({'mike':'hello'})

@page_blueprint.route('/page_details_<page_url>', methods=['POST', 'GET'])
#@jwt_required()
def get_page_details(page_url):
    user_id = current_identity
    page_url = page_url.replace("12___21","://")
    page_url = page_url.replace("13___31","/")
    #look up sites for this user and site
    page_details= Page.from_mongo_domain(page_url)
    return jsonify({'user_id': page_details[0].user_id, 'last_mod':page_details[0].last_mod, 'timestamp':page_details[0].timestamp, 'domain':page_details[0].domain,
                   'url':page_details[0].url,
                   'xss':page_details[0].xss,
                   'sqli':page_details[0].sqli,
                   'sql':page_details[0].sql,
                   'csrf':page_details[0].csrf,
                   'hash':page_details[0].hash,
                   'uptime':page_details[0].uptime,
                   'loadspeed':page_details[0].loadspeed,
                   'pagecontent':page_details[0].pagecontent,
                   'externallinks':page_details[0].externallinks,
                   'scripts':page_details[0].scripts,
                   'base64':page_details[0].base64,
                   'documenttype':page_details[0].documenttype,
                   'virus':page_details[0].virus,
                   'malware':page_details[0].malware,
                   'reputation':page_details[0].reputation,
                   'popups':page_details[0].popups,
                   'bruteforce':page_details[0].bruteforce,
                   'title':page_details[0].title,
                   'redirect':page_details[0].redirect,
                   'sensitivedata':page_details[0].sensitivedata,
                   'emailaddresses':page_details[0].emailaddresses,
                   'adaissues':page_details[0].adaissues,
                   'accesscontrol':page_details[0].accesscontrol,
                   'vulnerability':page_details[0].vulnerability,
                   'scanned':page_details[0].scanned})
