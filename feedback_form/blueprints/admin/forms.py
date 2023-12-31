#!/usr/bin/python3
"""This module contains forms for `admin` blueprint"""
from collections import OrderedDict

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from wtforms_alchemy import Unique

from lib.util_wtforms import ModelForm, choices_from_dict
from feedback_form.blueprints.user.models import db, User


class SearchForm(FlaskForm):
    q = StringField("Search terms", [Optional(), Length(1, 256)])


class BulkDeleteForm(FlaskForm):
    SCOPE = OrderedDict([
        ("all_selected_items", "All selected items"),
        ("all_search_results", "All search results")
        ])

    q = HiddenField("Search term", [Optional(), Length(1, 10)])

    scope = SelectField("Privileges", [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))


class UserForm(ModelForm):
    username_message = "Letters, numbers and underscores only please."

    username = StringField(validators=[
        Unique(User.username, get_session=lambda: db.session),
        Optional(),
        Length(1, 16),
        Regexp(r"^\w+$", message=username_message)
        ])

    role = SelectField("Privileges", [DataRequired()],
                       choices=choices_from_dict(User.ROLE,
                                                 prepend_blank=False))
    active = BooleanField("Yes, allow this user to sign in")
