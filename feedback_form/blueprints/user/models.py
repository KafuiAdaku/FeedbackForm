#!/usr/bin/python3
"""This module creates the `User` class to be mapped to the database"""
from datetime import datetime, timezone, timedelta
# from time import time
from collections import OrderedDict
from hashlib import md5

import pytz
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

from itsdangerous import URLSafeTimedSerializer
from authlib.jose import jwt, JsonWebToken
from authlib.jose.errors import DecodeError

from flask_login import UserMixin

from lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from feedback_form.extensions import db


class User(UserMixin, ResourceMixin, db.Model):
    """Definiton of `User` class"""
    ROLE = OrderedDict([
        ("member", "Member"),
        ("admin", "Admin"),
        ])

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    # authentication
    role = db.Column(db.Enum(*ROLE, name="role_types", native_enum=False),
                     index=True, nullable=False, server_default="member")
    active = db.Column("active", db.Boolean(), nullable=False, server_default="1")
    username = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False,
                      server_default="")
    password = db.Column(db.String(128), nullable=False, server_default="")


    # activity tracking
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))

    def __init__(self, **kwargs):
        # call Flask's SQLAlchemy constructor
        super(User, self).__init__(**kwargs)

        self.password = User.encrypt_password(kwargs.get("password", ""))
        # self.current_sign_in_on = datetime.now(tz=timezone.utc)
        # self.last_sign_in_on = self.current_sign_in_on


    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a user by their email or username

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        return User.query.filter((User.email == identity) |
                                 (User.username == identity)).first()

    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using PBKDF2.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str or None
        """
        if plaintext_password:
            return generate_password_hash(plaintext_password)
        return None

    @classmethod
    def deserialize_token(cls, token):
        """
        Obtain a user from de-serializing a signed token.

        :param token: Signed token.
        :type token: str
        :return: User instance or None
        """
        private_key = current_app.config["SECRET_KEY"]
        algorithm = "HS256"

        try:
            decode_payload = jwt.decode(token, private_key)
            return User.find_by_identity(decode_payload.get("user_email"))
        except DecodeError:
            return None


    @classmethod
    def initialize_password_reset(cls, identity):
        """
        Generate a token to reset the password for a specific user.

        :param identity: User e-mail address or username
        :type identity: str
        :return: User instance
        """
        user = User.find_by_identity(identity)
        reset_token = user.serialize_token()

        from feedback_form.blueprints.user.tasks import (
                deliver_password_reset_email)
        deliver_password_reset_email(user.id, reset_token)

        return user


    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return None

        search_query = f"%{query}%"
        search_chain = (User.email.ilike(search_query), User.username.ilike(search_query))

        return or_(*search_chain)


    @classmethod
    def is_last_admin(cls, user, new_role, new_active):
        """
        Determine whether or not this user is the last admin account.

        :param user: User being tested
        :type user: User
        :param new_role: New role being set
        :type new_role: str
        :param new_active: New active status being set
        :type new_active: bool
        :return: bool
        """
        is_changing_roles = user.role == 'admin' and new_role != 'admin'
        is_changing_active = user.active is True and new_active is None

        if is_changing_roles or is_changing_active:
            admin_count = User.query.filter(User.role == 'admin').count()
            active_count = User.query.filter(User.is_active is True).count()

            if admin_count == 1 or active_count == 1:
                return True


    def is_active(self):
        """
        Return whether or not the user account is active, this satisfies
        Flask-Login by overwriting the default value.

        :return: bool
        """
        return self.active


    def get_auth_token(self):
        """
        Return the user's auth token. Use their password as part of the token
        because if the user changes their password we will want to invalidate
        all of their logins across devices.

        This satisfies Flask-Login by providing a means to create a token.

        :return: str
        """
        private_key = current_app.config["SECRET_KEY"]
        serializer = URLSafeTimedSerializer(private_key)
        data = [str(self.id), md5(self.password.encode('utf-8')).hexdigest()]
        
        return serializer.dumps(data)


    def authenticated(self, with_password=True, password=""):
        """                                                                  
        Ensure a user is authenticated, and optionally check their password.                                                                                                    
                                                                             
        :param with_password: Optionally check their password                
        :type with_password: bool                                            
        :param password: Optionally verify this as their password            
        :type password: str                                                  
        :return: bool                                                        
        """
        if with_password:
            return check_password_hash(self.password, password)
        return True


    def serialize_token(self, expiration=3600):
        """
        Sign and create a token that can be used for things such as resetting
        a password or other tasks that involve a one off token.

        :param expiration: Seconds until it expires, defaults to 1 hour
        :type expiration: int
        :return: JSON
        """
        private_key = current_app.config["SECRET_KEY"]
        algorithm = "HS256"

        header = {"alg": algorithm, "typ": "JWT"}
        payload = {
                "iat": datetime.now(tz=timezone.utc),
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expiration),
                "user_email": self.email
                }
        token = jwt.encode(header, payload, private_key)
        
        return token


    def update_activity_tracking(self, ip_address):
        """
        Update various fields on the user that's related to meta data on their
        account, such as the sign in count and ip address, etc..

        :param ip_address: IP address
        :type ip_address: str
        :return: SQLAlchemy commit results
        """
        self.sign_in_count += 1

        self.last_sign_in_on = self.current_sign_in_on.replace(tzinfo=timezone.utc)
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_on = datetime.now(tz=timezone.utc)
        self.current_sign_in_ip = ip_address

        return self.save()
