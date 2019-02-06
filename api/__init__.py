"""creating app"""
from flask import Flask
from instance.config import app_config
from api.ver1.parties.endpoints import party_bp

def create_app(config_name):
    """ create flask app with specified configs """
    app = Flask(__name__, instance_relative_config=True) # instantiate the app

    # set configuration
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    ver_1_url_prefix = '/api/v1'

    #register parties blueprint
    app.register_blueprint(party_bp, url_prefix=ver_1_url_prefix)

    #register office blueprint
    #app.register_blueprint(office_blueprint, url_prefix=url_prefix_version_1)

    return app
