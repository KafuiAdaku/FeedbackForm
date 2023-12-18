from flask import Blueprint, render_template


page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def home():
    """
    Endpoint to render the home page.

    :return: Rendered template for the home page.
    """
    return render_template('page/home.html')


@page.route('/success')
def success_page():
    """
    Endpoint to render the success page.

    :return: Rendered template for the success page.
    """
    return render_template('page/success.html')


@page.route('/about')
def about_us():
    return render_template('page/about.html')
