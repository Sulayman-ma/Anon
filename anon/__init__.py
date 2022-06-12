from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail



db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    config_object.init_app()

    # extensions init
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .user import user
    from .admin import admin

    # blueprint registration
    app.register_blueprint(user)
    app.register_blueprint(admin)

    # app instance
    return app