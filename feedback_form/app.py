from flask import Flask, render_template
from celery import Celery
from itsdangerous import URLSafeTimedSerializer

from feedback_form.blueprints.admin import admin
from feedback_form.blueprints.page import page
from feedback_form.blueprints.feedback import feedback
from feedback_form.blueprints.user import user
from feedback_form.extensions import mail, db, migrate, csrf, login_manager
from feedback_form.blueprints.user.models import User

CELERY_TASK_LIST = [
    'feedback_form.blueprints.feedback.tasks',
    'feedback_form.blueprints.user.tasks'
    ]

def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app(settings_override=None):
    """
    Create a flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    # This line loads module from a config.settings.py file
    app.config.from_object("config.settings")

    # whiles this loads from a settings.py file from the instance dir
    app.config.from_pyfile("settings.py", silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(admin)
    app.register_blueprint(page)
    app.register_blueprint(feedback)
    app.register_blueprint(user)
    extensions(app)
    authentication(app, User)

    # Global 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('page/404.html'), 404

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the passed in).

    Example:
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    :param app: Flask application instance
    :return: None
    """

    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    return None


def authentication(app, user_model):
    """
    Initialize the Flask-Login extension (mutates the app passed in).

    :param app: Flask application instance
    :param user_model: Model that contains the authentication information
    :type user_model: SQLAlchemy model
    :return: None
    """
    login_manager.login_view = "user.login"

    @login_manager.user_loader
    def load_user(uid) :
        return user_model.query.get(uid)


    @login_manager.request_loader
    def load_from_request(request):
        token = request.headers.get('Authorization')
        if token:
            duration = app.config['REMEMBER_COOKIE_DURATION'].total_seconds()
            serializer = URLSafeTimedSerializer(app.secret_key)
            data = serializer.loads(token, max_age=duration)
            user_uid = data[0]
            return user_model.query.get(user_uid)
