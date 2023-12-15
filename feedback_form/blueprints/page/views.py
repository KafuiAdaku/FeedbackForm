from flask import Blueprint, render_template


page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def home():
    return render_template('page/home.html')


@page.route('/success')
def success_page():
    return render_template('page/success.html')

@page.route('/about')
def about_us():
    return render_template('page/about.html')
