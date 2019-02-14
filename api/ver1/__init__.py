from flask import Blueprint
from api.strings import ver_1_url_prefix

# Blueprints for version 1 and 2
v1 = Blueprint('api_ver1', __name__, url_prefix='/api/v1')
