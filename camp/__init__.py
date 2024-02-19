"""The configs directory acts as the package that will handle the configuration of the application as a whole.

Please note that any and all configuration for the application should reside here for easier configuration.
This also includes .secrets.<config_extension> that which is ignored by gitignore.
"""
import logging
import coloredlogs

from logging.config import dictConfig
from dynaconf import settings, FlaskDynaconf
from flask_login import LoginManager
from flask_mongoengine import MongoEngine, Document
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_mail import Mail
from flask_socketio import SocketIO


from flask_bcrypt import Bcrypt
from flask import Flask

logger = logging.getLogger(__name__)
flask_conf = FlaskDynaconf()
login_manager = LoginManager()

db = MongoEngine()
bcrypt = Bcrypt()
mail  = Mail()
socketio = SocketIO()


def create_app(config_file=None):
    """
    App factory.

    Create an application instance and return it.

    :param config_file: TODO: Future usecase for a config file based app instantiation.
    :return:
    """

    app = Flask(__name__, static_url_path='/static')
    
    app.config['SECRET_KEY'] = 'data'
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'sss@positivenaick.com'
    app.config['MAIL_PASSWORD'] = 'xxxxxxx'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    
    Bootstrap(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)

    CORS(app)

    # Initialize logs with custom config.
    dictConfig(settings.LOGGING_CONFIG)

    # Initialize colored logs.
    coloredlogs.install(level=logging.DEBUG)

    #Initialize Mongodb
    app.config['MONGODB_SETTINGS'] = {
    'db': 'camp',
    'host': "mongodb://"+settings.MONGO_HOST+":"+str(settings.MONGO_PORT)+"/camp"
    }
    db.init_app(app)

    # Registering api blueprint. 
    from camp.routes import api
    
    app.register_blueprint(api)
    login_manager.init_app(app)
    login_manager.login_view = 'CAMP.login'

    # Configuring dynaconf for app instance
    flask_conf.init_app(app)
    return app
