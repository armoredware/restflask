import uuid
from common.database import Database
from common.utils import Utils
import models.users.errors as UserErrors
import models.users.constants as UserConstants

__author__ = 'mjd'


class User(object):
    def __init__(self, email, password, domains, memberlevel, token, APIkey, config, name, paid, paymentdue, ads, products, company, address, city, state, zip, phone, _id=None):
        self.email = email
        self.password = password
        self.domains = domains
        self.memberlevel= memberlevel
        self.token= token
        self.APIkey= APIkey
        self.config= config
        self.name= name
        self.paid= paid
        self.paymentdue= paymentdue
        self.ads= ads
        self.products= products
        self.company= company
        self.address= address
        self.city= city
        self.state= state
        self.zip= zip
        self.phone= phone
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @classmethod
    def get_id(cls, email):
        user_data = Database.find_one("users", {"email": email})
        return user_data['_id']

    @classmethod
    def get_domains(cls, user_id):
        user_data = Database.find_one("users", {"_id": user_id})
        return user_data['domains']

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        user_data = Database.find_one("users", {"email": email})  # Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password, domains, memberlevel, token, APIkey, config, name, paid, paymentdue, ads, products, company, address, city, state, zip, phone):
        """
        This method registers a user using e-mail and password.
        The password already comes hashed as sha-512.
        :param email: user's e-mail (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        user_data = Database.find_one("users", {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")

        User(email, Utils.hash_password(password), domains, memberlevel, token, APIkey, config, name, paid, paymentdue, ads, products, company, address, city, state, zip, phone).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users", self.json())
    
    @staticmethod
    def update_domains(user, domain):
        Database.update_set("users",{ "_id" : user }, { "$addToSet" : { "domains" :  domain}  });


    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "domains": self.domains,
            "memberlevel": self.memberlevel,
            "token": self.token,
            "APIkey": self.APIkey,
            "config": self.config,
            "name": self.name,
            "paid": self.paid,
            "paymentdue": self.paymentdue,
            "ads": self.ads,
            "products": self.products,
            "company": self.company,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "phone": self.phone
        }

    def get_alerts(self):
        #return self.find_by_email(self.email)
        #return render_template('/wines/admin_search.html')
        #return user=User.get_by_email(session['email'])
        return None
