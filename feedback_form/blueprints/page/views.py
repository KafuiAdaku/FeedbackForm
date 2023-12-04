from flask import Blueprint, render_template


page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def home():
    return render_template('page/home.html')


@page.route('/success')
def success_page():
    return render_template('page/success.html')


# @page.errorhandler(404)
# def page_not_found(e):
#     return render_template('page/404.html'), 404