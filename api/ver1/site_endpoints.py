from flask import Blueprint
from api.strings import status_key, status_200
from api.ver1.utils import success, error

route_bp = Blueprint('route', __name__) # init the blueprint for Heroku online

@route_bp.route('/')
@route_bp.route('/index')
def index():
    """ Index Page for API """
    return success(code=status_200, data='Howdy! Welcome to the gVotie API')
