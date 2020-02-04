from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    db.app = app
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .results import results_blueprint
    app.register_blueprint(results_blueprint)

    from .courses import courses_blueprint
    app.register_blueprint(courses_blueprint)

    from .mangements import managements_blueprint
    app.register_blueprint(managements_blueprint)

    from .control_room import control_room_blueprint
    app.register_blueprint(control_room_blueprint)

    return app













