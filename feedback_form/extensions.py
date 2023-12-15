from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()
