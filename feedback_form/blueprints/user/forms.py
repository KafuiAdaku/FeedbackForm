#!/usr/bin/python3
"""Module defining forms for user login"""
from flask_wtf import FlaskForm
from wtforms import (HiddenField, StringField, PasswordField, BooleanField)
from wtforms.validators import (DataRequired, Email, Length,
                                Optional, Regexp)
from wtforms_alchemy import Unique

from lib.util_wtforms import ModelForm
from feedback_form.blueprints.user.models import User, db
from feedback_form.blueprints.user.validations import ensure_identity_exists, \
        ensure_existing_password_matches


class LoginForm(FlaskForm):
    next = HiddenField()
    identity = StringField("Username or Email",
                           [DataRequired(), Length(3, 256)])
    password = PasswordField("Password", [DataRequired(), Length(8, 128)])
    remember = BooleanField("Stay signed in")


class BeginPasswordResetForm(FlaskForm):
    identity = StringField("Username or email",
                           [DataRequired(),
                            Length(8, 256),
                            ensure_identity_exists])


class PasswordResetForm(FlaskForm):
    reset_token = HiddenField()
    password = PasswordField("Password", [DataRequired(), Length(8, 128)])


class SignUpForm(ModelForm):
    email = StringField("Email", [DataRequired(), Email(),
                        Unique(User.email, get_session=lambda: db.session)])
    password = PasswordField("Password", [DataRequired(), Length(8, 128)])


class WelcomeForm(ModelForm):
    username_message = "Letters, numbers and underscores only please."

    username = StringField(validators=[
                           Unique(User.username,
                                  get_session=lambda: db.session),
                           DataRequired(),
                           Length(1, 16),
                           Regexp(r"^\w+$", message=username_message)
                           ])


class UpdateCredentials(ModelForm):
    current_password = PasswordField("Current password",
                                     [DataRequired(),
                                      Length(8, 128),
                                      ensure_existing_password_matches])
    email = StringField(validators=[
                        Email(),
                        Unique(User.email, get_session=lambda: db.session)]
                        )
    password = PasswordField("Password", [Optional(), Length(8, 128)])
