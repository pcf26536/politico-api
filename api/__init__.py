"""creating app"""
from flask import Flask, jsonify
from instance.config import app_config
from api.ver1.offices.endpoints import office_v1
from api.ver1.parties.endpoints import party_v1
from api.ver2.endpoints.auth import auth
from api.site_endpoints import route_bp
from api.strings import status_400, status_404, status_405
from api.ver2.database.model import Database
from flask_jwt_extended import JWTManager
from .strings import *


def create_app(config_name):
    """ create flask app with specified configs """
    if not config_name:
        config_name = 'production'

    app = Flask(__name__, instance_relative_config=True) # instantiate the app

    # set configuration
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # register error handler blueprints
    app.register_blueprint(route_bp)

    #register v1 blueprints
    app.register_blueprint(office_v1, url_prefix=ver_1_url_prefix)
    app.register_blueprint(party_v1, url_prefix=ver_1_url_prefix)

    #register v2 blueprints
    app.register_blueprint(auth,  url_prefix=ver_2_url_prefix)

    # DB initializer
    db = Database(config_name)
    db.connect()
    db.create_db_tables()
    db.create_root_user()

    jwt = JWTManager(app)

    @app.errorhandler(status_400)
    def bad_request(error):
        """ Handle error 400 """
        return jsonify({'message': 'Please review your request and try again', 'status': 400})

    @app.errorhandler(status_404)
    def page_not_found(error):
        """ Handle error 404 """
        return jsonify({'message': 'The requested resource was not found', 'status': 404})

    @app.errorhandler(status_405)
    def method_not_allowed(error):
        """ Handle error 405 """
        return jsonify({'message': 'Method not allowed', 'status': 405})

    return app
