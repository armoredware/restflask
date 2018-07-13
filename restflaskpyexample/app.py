__author__='mjd'

from flask import Flask, jsonify, request, send_file, render_template
from flask_jwt import JWT, jwt_required, current_identity
from urlparse import urlparse, urlunparse 
from common.database import Database
import subprocess
import urllib2
import telnetlib
import time
#from flask_cors import CORS, cross_origin
from models.users.user import User
import models.users.errors as UserErrors
import models.users.decorators as user_decorators
 
class Userjwt(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
 
    def __str__(self):
        return "User(id='%s')" % self.id
 
user = Userjwt(str(1), 'admin1221', 'admin1221')
#username_table = {u.username: u for u in users}
#userid_table = {u.id: u for u in users} 

#@app.before_request
#def redirect_nonwww():
#    """Redirect non-www requests to www."""
#    urlparts = urlparse(request.url)
#    if urlparts.netloc == 'armoredware.com':
#        urlparts_list = list(urlparts)
#        urlparts_list[1] = 'www.armoredware.com'
#        return redirect(urlunparse(urlparts_list), code=301)


def authenticate(username, password):
    #user = Userjwt(3, str(username), str(password))
    if User.is_login_valid(username, password):
        idvar = User.get_id(username)
        user = Userjwt(str(idvar), str(username), str(password))

    if username == user.username and password == user.password:
        return user
    #user = username_table.get(username, None)
    #if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
    #    return user
    #try:
    #    if User.is_login_valid(username, password):
    #	    return user
    #except Exception, e:
        return jsonify({'access_token': 'Error, ' + str(e) })
 
def identity(payload):
    #return user
    #pass
    user_id = payload['identity']
    #return userid_table.get(user_id, None)
    return user_id
 
app = Flask(__name__)
app.debug = True
app.config['SERVER_NAME']= 'armoredware.com'
app.config['SECRET_KEY'] = 'super-secret'
#CORS(app)

 
jwt = JWT(app, authenticate, identity)
 

@app.before_first_request
def init_db():
     Database.initialize()

 
# send CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
 
 
@app.route('/unprotected')
def unprotected():
    test_var = str(app.url_map)
    return jsonify({
        'message': 'This is an unprotected resource ' + test_var
    })
 
 
@app.route('/protected')
@jwt_required()
def protected():
    #'current_identity': str(current_identity)
    return jsonify({
        'message': 'This is a protected resource.',
        'current_identity': str(current_identity)
    })


#@app.route('/')
#def indexwww():
#    return send_file('downloads.html')


#@app.route('/',subdomain='www')
@app.route('/')
@app.route('/', subdomain='www')
def index():
    return send_file('index.html')
    #return "Hello"
    #return render_template('app.html')

@app.route('/virus', methods=["GET","POST"])
def virus():
    if request.method == "POST":
        #name = request.form["name"]
        name = request.json["name"]
        return jsonify({'name': 'Welcome ' + name })
    else:
        return jsonify({'message' : 'Not available'}) 
    #return jsonify({'virus': hash})
    #return hash

#NGINX forwarded by HTTP_X_FORWARDED_FOR
@app.route("/ip", methods=["GET"])
def ip():
    ip_addr = request.remote_addr
    ping = subprocess.Popen(["ping",ip_addr,"-c", "1","-W","2"],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    ping_data = ping.communicate()[0]    
    time.sleep(1)
    nslookup = subprocess.Popen(["nslookup",ip_addr],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    nslookup_data = nslookup.communicate()[0]
    time.sleep(1)
    traceroute = subprocess.Popen(["traceroute",ip_addr],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    traceroute_data = traceroute.communicate()[0]
    time.sleep(1)
    rdns = subprocess.Popen(["host",ip_addr],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    rdns_data = rdns.communicate()[0]
    time.sleep(1)
    telnetd = subprocess.Popen(["telnet",ip_addr],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    telnet_data = telnetd.communicate()[0]
    time.sleep(1)
    return jsonify({'ip': ip_addr, 'ip_accessroute':  request.access_route[0], 'header': str(request.headers), 'ping': ping_data, 'nslookup':nslookup_data, 'rdns': rdns_data, 'traceroute': traceroute_data, 'telnet': telnet_data }), 200

@app.route('/armoredeyes')
def armoredeyes():
    return jsonify({
        'message': 'Welcome to the server'
    })

#blueprint
from models.users.views import user_blueprint
from models.pages.views import page_blueprint
#from models.wines.views import wine_blueprint
#from models.blogs.views import blog_blueprint
#from models.posts.views import post_blueprint
from models.sites.views import site_blueprint
#from models.pages.views import page_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(page_blueprint, url_prefeix="/pages")
#app.register_blueprint(wine_blueprint, url_prefix="/wines")
#app.register_blueprint(blog_blueprint, url_prefix="/blogs")
#app.register_blueprint(post_blueprint, url_prefix="/posts")
app.register_blueprint(site_blueprint, url_prefix="/sites")
#app.register_blueprint(page_blueprint, url_prefeix="/pages")

if __name__ == '__main__':
    app.run(host='23.254.247.82', debug = True, port=5002)
