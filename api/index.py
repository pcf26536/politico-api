from flask import Blueprint
from api.strings import status_200
from api.ver1.utils import success
from api.strings import ver_2_url_prefix, ver_1_url_prefix

route_bp = Blueprint('route', __name__) # init the blueprint for Heroku online


@route_bp.route('/')
@route_bp.route('/index')
def index():
    """ Index Page for API """
    return success(
        code=status_200,
        data=[
            'Howdy! Welcome to the gVotie API - Available Endpoints',
            {'SignUp': ver_2_url_prefix + '/auth/signup', 'method': 'POST'},
            {'Login': ver_2_url_prefix + '/auth/login', 'method': 'POST'},
            {'Rest Password': ver_2_url_prefix + '/auth/reset', 'method': 'POST'},

            {'Get Parties v1': ver_1_url_prefix + '/parties', 'method': 'GET'},
            {'Get Party v1': ver_1_url_prefix + '/parties/<int:id>', 'method': 'GET'},
            {'Get Parties v2': ver_2_url_prefix + '/parties', 'method': 'GET'},
            {'Add Party v1': ver_1_url_prefix + '/parties', 'method': 'POST'},
            {'Add Party v2': ver_2_url_prefix + '/parties', 'method': 'POST'},
            {'Get Party v2': ver_2_url_prefix + '/parties/<int:id>', 'method': 'GET'},
            {'Delete Party v2': ver_2_url_prefix + '/parties/<int:id>', 'method': 'DELETE'},

            {'Add Office v1': ver_1_url_prefix + '/offices', 'method': 'POST'},
            {'Add Office v2': ver_2_url_prefix + '/offices', 'method': 'POST'},
            {'Get Offices v1': ver_1_url_prefix + '/offices', 'method': 'GET'},
            {'Get Office v1': ver_1_url_prefix + '/offices/<int:id>', 'method': 'GET'},
            {'Get Offices v2': ver_2_url_prefix + '/offices', 'method': 'GET'},
            {'Add Office v1': ver_1_url_prefix + '/offices', 'method': 'POST'},
            {'Add Office v2': ver_2_url_prefix + '/offices', 'method': 'POST'},
            {'Get Office v2': ver_2_url_prefix + '/offices/<int:id>', 'method': 'GET'},
            {'Delete Office v2': ver_2_url_prefix + '/offices/<int:id>', 'method': 'DELETE'},

            {'Vote': ver_2_url_prefix + '/votes/', 'method': 'POST'},

            {'Register Candidates': ver_2_url_prefix + '/office/<int:id>/register', 'method': 'POST'},
            {'Get All Candidates': ver_2_url_prefix + '/office/<int:id>/register', 'method': 'GET'},

            {'Get All Results': ver_2_url_prefix + '/votes/', 'method': 'GET'},
            {'Get Specific Candidate Votes': ver_2_url_prefix + '/votes/<int:id>', 'method': 'GET'},
            {'Get Specific Office Results': ver_2_url_prefix + '/office/<int:id>/result', 'method': 'GET'},

            {'Create Petition': ver_2_url_prefix + '/petitions/', 'method': 'POST'},
        ])
