"""creating app"""
from flask import Flask, jsonify, request
from instance.config import app_config
from api.ver1.offices.endpoints import office_v1
from api.ver1.parties.endpoints import party_v1
from api.ver2.endpoints.auth import auth
from api.index import route_bp
from api.ver2.endpoints.offices import office_v2
from api.ver2.endpoints.parties import party_v2
from api.ver2.endpoints.petitions import petitions_bp
from api.ver2.endpoints.vote import vote_bp
from api.ver2.endpoints.candidature import candids
from api.strings import status_400, status_404, status_405
from api.ver2.database.model import Database
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from flask_cors import CORS
from .strings import *
import os


def create_app(config_name):
    """ create flask app with specified configs """
    app = Flask(__name__, instance_relative_config=True)

    # set configuration
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')

    # candids error handler blueprints
    app.register_blueprint(route_bp)

    # candids v1 blueprints
    app.register_blueprint(office_v1, url_prefix=ver_1_url_prefix)
    app.register_blueprint(party_v1, url_prefix=ver_1_url_prefix)

    # candids v2 blueprints
    app.register_blueprint(auth,  url_prefix=ver_2_url_prefix)
    app.register_blueprint(candids, url_prefix=ver_2_url_prefix)
    app.register_blueprint(office_v2, url_prefix=ver_2_url_prefix)
    app.register_blueprint(party_v2, url_prefix=ver_2_url_prefix)
    app.register_blueprint(petitions_bp, url_prefix=ver_2_url_prefix)
    app.register_blueprint(vote_bp, url_prefix=ver_2_url_prefix)

    # DB initializer
    db = Database(config_name)
    db.connect()
    db.create_db_tables()
    db.create_root_user()

    CORS(app)
    jwt = JWTManager(app)
    mail = Mail(app)  # Create an instance of Mail class.

    @app.route('/mailer', methods=['POST'])
    def mailer():
        data = request.get_json()
        msg = Message(
            data['subject'],
            recipients=data['recipients'],
            sender=os.getenv('MAIL_USERNAME')
        )
        msg.body = data['body']
        mail.send(msg)

    @app.errorhandler(status_400)
    def bad_request(error):
        """ Handle error 400 """
        return jsonify(
            {'message': 'Please review your request and try again',
             'status': 400
             })

    @app.errorhandler(status_404)
    def page_not_found(error):
        """ Handle error 404 """
        return jsonify(
            {'message': 'The requested resource was not found', 'status': 404}
        )

    @app.errorhandler(status_405)
    def method_not_allowed(error):
        """ Handle error 405 """
        return jsonify({'message': 'Method not allowed', 'status': 405})

    @app.errorhandler(500)
    def sys_unavailable(error):
        return jsonify(
            {
                'message': 'System not available, try again later!',
                'status': 500
             }
        )

    @jwt.expired_token_loader
    def expired_token_callback(expired_token):
        token_type = expired_token['type']
        return jsonify({
            'status': 401,
            'error': 'The {} token has expired'.format(token_type)
        }), 401

    return app
