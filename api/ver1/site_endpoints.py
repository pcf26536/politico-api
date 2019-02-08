from flask import Blueprint
from api.strings import status_key, status_200, status_400, status_404, status_405
from api.ver1.utils import success, error

route_bp = Blueprint('route', __name__) # init the blueprint for Heroku online

@route_bp.route('/')
@route_bp.route('/index')
def index():
    """ Index Page for API """
    return success(code=status_200, data='Howdy! Welcome to the gVotie API')

@route_bp.errorhandler(status_400)
def bad_request(error):
    """ Handle error 400 """
    return error(message='Please review your request and try again', code=status_400)

@route_bp.errorhandler(status_404)
def page_not_found(error):
    """ Handle error 404 """
    return error(message='The requested resource was not found', code=status_404)

@route_bp.errorhandler(status_405)
def method_not_allowed(error):
    """ Handle error 405 """
    return error(message='Method not allowed', code=status_405)
