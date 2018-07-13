from flask import Blueprint, request, session, url_for, render_template, jsonify
from werkzeug.utils import redirect
from models.users.user import User
import models.users.errors as UserErrors
import models.users.decorators as user_decorators
from urlparse import urlparse, urlunparse
import urllib2

__author__ = 'mjd'


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email = request.json["email"]
        password = request.json["password"]

        try:
            if User.is_login_valid(email, password):
                #session['email'] = email
                #return redirect(url_for(".user_alerts"))
                return jsonify({'email': email })
        except UserErrors.UserError as e:
            return jsonify({'error': 'Error, ' + e.message })
            #return jsonify({'error': 'Failed Try Again' })

    return render_template("users/login.jinja2")  # Send the user an error if their login was invalid
    #return jsonify({'error': 'Please Login'})

@user_blueprint.route('/register', methods=['GET', 'POST'])
#@user_decorators.requires_login #mike added
def register_user():
    #user = User.find_by_email(session['email']) #mike added
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        #domains = request.json['domains']
        domains = []
        memberlevel= request.json['memberlevel']
        token= request.json['token']
        APIkey= request.json['APIkey']
        config= request.json['config']
        name= request.json['name']
        paid= request.json['paid']
        paymentdue= request.json['paymentdue']
        ads= request.json['ads']
        products= request.json['products']
        company= request.json['company']
        address= request.json['address']
        city= request.json['city']
        state= request.json['state']
        zip= request.json['zip']
        phone= request.json['phone']

        try:
            if User.register_user(email, password, domains, memberlevel, token, APIkey, config, name, paid, paymentdue, ads, products, company, address, city, state, zip, phone):
                #session['email'] = email
                #return redirect(url_for(".user_alerts"))
                return jsonify({ 'username': str(email), 'password': str(password) })
        except UserErrors.UserError as e:
            #return e.message
            return jsonify({ 'username': str(e), 'password': 'no' })

    #return render_template("users/register.jinja2")  # Send the user an error if their login was invalid
    return jsonify({ 'access_token': 'fail' })

@user_blueprint.route('/edit_profile/<string:_id>', methods=['POST', 'GET'])
#@user_decorators.requires_login #mike added
def edit_profile(_id):
    profile = User.from_mongo_id(_id)
    if request.method == 'GET':
        return jsonify({"id": str(_id), "user": str(profile)})
    else:
        email = request.json['email']
        password = request.json['password']
        domains = request.json['domains']
        memberlevel= request.json['memberlevel']
        token= request.json['token']
        APIkey= request.json['APIkey']
        config= request.json['config']
        name= request.json['name']
        paid= request.json['paid']
        paymentdue= request.json['paymentdue']
        ads= request.json['ads']
        products= request.json['products']
        company= request.json['company']
        address= request.json['address']
        city= request.json['city']
        state= request.json['state']
        zip= request.json['zip']
        phone= request.json['phone']

        edited_site = Site(email, password, domains, memberlevel, token, APIkey, config, name, paid, paymentdue, ads, products, company, address, city, state, zip, phone, site_id)
        edited_site.update_to_mongo()
        return jsonify({"message": "Profile Updated"})


@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    return render_template("users/alerts.jinja2", alerts=user.get_alerts(), email=user.email)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    #return redirect(url_for('home'))
    return redirect(url_for('users.login_user'))


@user_blueprint.route('/check_alerts/<string:user_id>')
@user_decorators.requires_login
def check_user_alerts(user_id):
    pass
