from flask import Blueprint, request, session, url_for, render_template, jsonify
from werkzeug.utils import redirect
from models.sites.site import Site
from models.pages.page import Page
import models.sites.errors as SiteErrors
from models.users.user import User
import models.users.decorators as user_decorators
from flask_jwt import jwt_required, current_identity
import subprocess
import urllib2
import telnetlib
import time

__author__ = 'mjd'


site_blueprint = Blueprint('sites', __name__)

@site_blueprint.route('/add_site', methods=['POST', 'GET'])
@jwt_required()
def add_site():
    site_url = request.json['site_url']
    user_id = str(current_identity)
    get_pageList = subprocess.Popen(["python3.5","/var/www/py/armoredware.com/infosec/get_pageList.py","--domain",site_url],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    pageList = get_pageList.communicate()[0]
    time.sleep(1)
    pageList = pageList.replace("'", '')
    pageList = pageList.replace('\n', '')
    pageList = pageList[:-1]
    pageList= pageList.split(",")

    #add page documents to mongodb here
    for page in pageList:
        domain = site_url
        timestamp = time.time()
        url = page    
        last_mod = None
        xss= None
        sqli= None
        sql= None
        csrf= None
        hash= None
        uptime= None
        loadspeed= None
        pagecontent= None
        externallinks= None
        scripts= None
        base64= None
        documenttype= None
        virus= None
        malware= None
        reputation= None 
        popups= None
        bruteforce= None
        title= None
        redirect= None
        sensitivedata= None
        emailaddresses= None
        adaissues= None
        accesscontrol= None
        vulenrability= None
        scanned= None
        new_page = Page(domain, user_id, last_mod, timestamp,
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
                   vulenrability,
                   scanned)
        new_page.save_to_mongo()
    
    #object encoding error not sure why this is happening string maybe? happens in both edited_site and update_domain
    edited_site= Site.from_mongo_domain(site_url)
    edited_site[0].user_id= user_id
    #edited_site[0].pagecount= pagecount
    #edited_site[0].pageList= pageList
    edited_site[0].verified= "true"
    edited_site[0].paid= "true"
    edited_site[0].timestamp= time.time()
    edited_site[0].update_to_mongo()

    User.update_domains(user_id,site_url)
    
    
    
    return jsonify({'success':'yes'})

@site_blueprint.route('/start_scan')
def start_scan():
    site_url = 'http://www.rolfny.com'
    #return jsonify({'site':str(site_url)})
    site= Site.from_mongo_domain(site_url)
    try:
        site[0].scan_ip()
        #return jsonify({'scan_ip':'success'})
    except Exception as e:    
        return jsonify({'scan_ip':str(e)})
    try:
        site[0].scan_speed()
        #return jsonify({'scan_speed':'success'})
    except Exception as e:
        return jsonify({'scan_speed':str(e)})
    return jsonify({'scan':'success'})

@site_blueprint.route('/testscan_os', methods=['POST','GET'])
def testscan_os():
    site_url = "http://www.rolfny.com"
    #site= Site.from_mongo_domain(site_url)
    #osInfo= site[0].scan_os()
    #subprocess.Popen(["python3.5","/var/www/py/armoredware.com/infosec/blackops/wig.py","-u",site_url,"&"],stdout = subprocess.PIPE,stderr = subprocess.PIPE, shell = True)
    #get_osInfo.wait()
    #time.sleep(60)
    #osInfo = get_osInfo.communicate()[0]
    #get_osInfo.wait()
    #time.sleep(60)
    return jsonify({'site': 'lets go'})

@site_blueprint.route('/get_quote', methods=['POST', 'GET'])
@jwt_required()
def get_quote():
    site_url = request.json['site_url']
    user_id = current_identity
    #quote = 39
    #pages = 50
    error = 'None'
    get_pageList = subprocess.Popen(["python3.5","/var/www/py/armoredware.com/infosec/get_pageList.py","--domain",site_url],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    pageList = get_pageList.communicate()[0]
    time.sleep(1)
    pageList = pageList.replace("'", '')
    pageList = pageList.replace('\n', '')
    pageList = pageList[:-1]
    pagecount = pageList.count("://")
    #does site exist in our database
    #count pages
    #give quote
    quote = 5+(.75 * pagecount)
    #site = Site.from_mongo(search_phrase, search_type, search_vintage, search_bottle, search_country, search_case)
    

    pageList= pageList.split(",")
    #if site with this domain does not exist create it else look up the site.
    name= None
    domain= str(site_url)
    user_id= str(user_id)
    uptime= None
    alerts= None
    verbosity= None
    alias= None
    os= None
    middleware= None
    database= None
    platform= None
    cms= None
    appfirewall= None
    loadspeed= None
    vulnerabilities= None
    adacompliance= None
    virus= None
    malware= None
    pagerank= None
    backlinks= None
    ipaddress= None
    ports= None
    bruteforce= None
    traceroute= None
    price= quote
    seal= None
    paid= 'false'
    verified= 'false'
    html= None
    js= None
    title= None
    thumbnail= None
    scanned= None
    resources= pagecount
    pages= pageList
    timestamp= time.time()
    isLatest= None
    
    #need to add if else site exists and is paid/verified do nothing
        
    if Site.site_exists(site_url):
        edited_site= Site.from_mongo_domain(site_url)
        edited_site[0].user_id= user_id
        #edited_site[0].pagecount= pagecount
        #edited_site[0].pageList= pageList
        edited_site[0].timestamp= time.time()
        edited_site[0].update_to_mongo()
    else:
        new_site = Site(name, domain, user_id,
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
                            resources, pages, timestamp, isLatest)
        new_site.save_to_mongo()
    
    return jsonify({'user_id': str(user_id), 'site_url': str(site_url), 'quote': str(quote), 'pages': pageList, 'error': str(error)})

@site_blueprint.route('/get_sites', methods=['POST', 'GET'])
@jwt_required()
def get_sites():
    user_id = str(current_identity)
    #look up sites for this user
    domains = User.get_domains(user_id)
    return jsonify({'user_id': user_id, 'sites': domains })

@site_blueprint.route('/test_sub', methods=['POST', 'GET'])
def test_sub():
    site_url = 'http://www.ridgewaynsk.com'
    get_pageList = subprocess.Popen(["python3.5","/var/www/py/armoredware.com/infosec/get_pageList.py","--domain",site_url],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    pageList = get_pageList.communicate()[0]
    time.sleep(1)
    pageList = pageList.replace('\n', '')
    pageList = pageList[:-1]
    pagecount = pageList.count("://")
    return jsonify({'pagecount':str(pagecount),'pages':[pageList]})

@site_blueprint.route('/site_details_<site_url>', methods=['POST', 'GET'])
@jwt_required()
def get_site_details(site_url):
    user_id = current_identity
    site_url = site_url.replace("12___21","://")
    #look up sites for this user and site
    site_details= Site.from_mongo_domain(site_url)
    return jsonify({'user_id': str(user_id), 
        'site_url': site_details[0].verified,
        'name': site_details[0].name, 
        'domain': site_details[0].domain,
        'uptime': site_details[0].uptime,
        'alerts': site_details[0].alerts,
        'verbosity': site_details[0].verbosity,
        'alias': site_details[0].alias,
        'os': site_details[0].os,
        'middleware': site_details[0].middleware,
        'database': site_details[0].database,
        'platform': site_details[0].platform,
        'cms': site_details[0].cms,
        'appfirewall': site_details[0].appfirewall,
        'loadspeed': site_details[0].loadspeed,
        'vulnerabilities': site_details[0].vulnerabilities,
        'adacompliance': site_details[0].adacompliance,
        'virus': site_details[0].virus,
        'malware': site_details[0].malware,
        'pagerank': site_details[0].pagerank,
        'backlinks': site_details[0].backlinks,
        'ipaddress': site_details[0].ipaddress,
        'ports': site_details[0].ports,
        'bruteforce': site_details[0].bruteforce,
        'traceroute': site_details[0].traceroute,
        'price': site_details[0].price,
        'seal': site_details[0].seal,
        'paid': site_details[0].paid,
        'verified': site_details[0].verified,
        'html': site_details[0].html,
        'js': site_details[0].js,
        'title': site_details[0].title,
        'thumbnail': site_details[0].thumbnail,
        'scanned': site_details[0].scanned,
        'resources': site_details[0].resources, 
        'pages': site_details[0].pages, 
        'timestamp': site_details[0].timestamp,
        'isLatest': site_details[0].isLatest})


@site_blueprint.route('/site_search')
def search_template():
    #User.update_domains("56852d536ab94a06a3f3a10d260fefb0","rolfny.com")
    testvar = "hello"
    return jsonify({'message': testvar})

@site_blueprint.route('/admin/site_search')
@user_decorators.requires_login #mike added
def admin_search():
    return render_template('/sites/admin_search.html')

@site_blueprint.route('/site_search_results', methods=['POST'])
def search_results():
    search_phrase = request.form['search_phrase']
    search_type = request.form['search_type']
    search_vintage= request.form['search_vintage']
    search_bottle= request.form['search_bottle']
    search_country= request.form['search_country']
    search_case= request.form['search_case']
    
    site = Site.from_mongo(search_phrase, search_type, search_vintage, search_bottle, search_country, search_case)
    return render_template('/sites/search_results.html', search_phrase= search_phrase, site= site)


@site_blueprint.route('/admin/site_search_results', methods=['POST'])
@user_decorators.requires_login #mike added
def admin_search_results():
    search_phrase = request.form['search_phrase']
    search_type = request.form['search_type']
    search_vintage= request.form['search_vintage']
    search_bottle= request.form['search_bottle']
    search_country= request.form['search_country']
    search_case= request.form['search_case']
    
    site = Site.from_mongo(search_phrase, search_type, search_vintage, search_bottle, search_country, search_case)
    return render_template('/sites/admin_search_results.html', search_phrase= search_phrase, site= site)

@site_blueprint.route('/admin/new_site', methods=['POST', 'GET'])
@user_decorators.requires_login #mike added
def create_new_site():
    if request.method == 'GET':
        return render_template('/sites/new_site.html')
    else:
        name= request.form['name']
        domain= request.form['domain']
        user_id= request.form['user_id']
        uptime= request.form['uptime']
        alerts= request.form['alerts']
        verbosity= request.form['verbosity']
        alias= request.form['alias']
        os= request.form['os']
        middleware= request.form['middleware']
        database= request.form['database']
        platform= request.form['platform']
        cms= request.form['cms']
        appfirewall= request.form['appfirewall']
        loadspeed= request.form['loadspeed']
        vulnerabilities= request.form['vulnerabilities']
        adacompliance= request.form['adacompliance']
        virus= request.form['virus']
        malware= request.form['malware']
        pagerank= request.form['pagerank']
        backlinks= request.form['backlinks']
        ipaddress= request.form['ipaddress']
        ports= request.form['ports']
        bruteforce= request.form['bruteforce']
        traceroute= request.form['traceroute']
        price= request.form['price']
        seal= request.form['seal']
        paid= request.form['paid']
        verified= request.form['verified']
        html= request.form['html']
        js= request.form['js']
        title= request.form['title']
        thumbnail= request.form['thumbnail']
        scanned= request.form['scanned']
        resources= request.form['resources']
        pages= request.form['pages']
        timestamp= request.form['timestamp']
        isLatest= ['isLatest']


        new_site = Site(name, domain, user_id,
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
                resources, pages, timestamp, isLatest)
        new_site.save_to_mongo()

        #return make_response("Thanks", 200)
        #return render_template('search.html')
        return render_template('/sites/added_site.html')

@site_blueprint.route('/admin/edit_site/<string:site_id>', methods=['POST', 'GET'])
@user_decorators.requires_login #mike added
def edit_site(site_id):
    site = Site.from_mongo_id(site_id)
    if request.method == 'GET':
        
        return render_template('/sites/edit_site.html', site_id=site_id, site= site)
    else:
        name= request.form['name']
        domain= request.form['domain']
        user_id= request.form['user_id']
        uptime= request.form['uptime']
        alerts= request.form['alerts']
        verbosity= request.form['verbosity']
        alias= request.form['alias']
        os= request.form['os']
        middleware= request.form['middleware']
        database= request.form['database']
        platform= request.form['platform']
        cms= request.form['cms']
        appfirewall= request.form['appfirewall']
        loadspeed= request.form['loadspeed']
        vulnerabilities= request.form['vulnerabilities']
        adacompliance= request.form['adacompliance']
        virus= request.form['virus']
        malware= request.form['malware']
        pagerank= request.form['pagerank']
        backlinks= request.form['backlinks']
        ipaddress= request.form['ipaddress']
        ports= request.form['ports']
        bruteforce= request.form['bruteforce']
        traceroute= request.form['traceroute']
        price= request.form['price']
        seal= request.form['seal']
        paid= request.form['paid']
        verified= request.form['verified']
        html= request.form['html']
        js= request.form['js']
        title= request.form['title']
        thumbnail= request.form['thumbnail']
        scanned= request.form['scanned']
        resources= request.form['resources']
        pages= request.form['pages']
        timestamp= request.form['timestamp']
        isLatest= ['isLatest']

        edited_site = Site(name, domain, user_id,
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
                   resources, pages, timestamp, isLatest, site_id)
        edited_site.update_to_mongo()

        return render_template('/sites/updated_site.html')

@site_blueprint.route('/admin/remove_site/<string:site_id>', methods=['GET'])
@user_decorators.requires_login #mike added
def remove_site(site_id):
    site = Site.remove_from_mongo_id(site_id)
    #if request.method == 'GET':
        
    return render_template('/sites/deleted_site.html')
    '''else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))'''

@site_blueprint.route('/miketest', methods=['GET'])
def show_site_url():
    site_url = 'http://www.ridgewaynsk.com'
    #site = Site.from_mongo_domain(site_url)
    if Site.site_exists(site_url):
        return jsonify({'site_exists':'it works'})
    else:
        return jsonify({'site_exists':'no'})
    #if request.method == 'GET':
    #return jsonify(site[0].json())

@site_blueprint.route('/site_details/<string:site_id>', methods=['GET'])
def show_site(site_id):
    site = site.from_mongo_id(site_id)
    #if request.method == 'GET':
        
    return render_template('/sites/details.html', site_id=site_id, site= site)
    '''else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))'''


'''@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    return render_template("users/alerts.jinja2", alerts=user.get_alerts())


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('/check_alerts/<string:user_id>')
@user_decorators.requires_login
def check_user_alerts(user_id):
    pass'''
