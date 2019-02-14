from flask import Blueprint

# Blueprints for version 1 and 2
v1 = Blueprint('api_ver1', __name__)
v2 = Blueprint('api_ver2', __name__)