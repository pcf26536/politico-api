from flask import Blueprint, redirect
from api.strings import status_200
from api.ver1.utils import success

route_bp = Blueprint('route', __name__)


@route_bp.route('/')
@route_bp.route('/index')
def index():
    """ Index Page for API """
    return success(
        code=status_200,
        data=[
                'Howdy! Welcome to the gVotie API - Available Endpoints'
            ]
        )


@route_bp.route('/docs')
def docs():
    return redirect('https://gvotie.docs.apiary.io')
