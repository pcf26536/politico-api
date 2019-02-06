from flask import Blueprint, jsonify, request
from api.ver1.utils import error, success
from api.ver1.parties.controllers import Party
from api.strings import *
from .strings import *

party_bp = Blueprint('parties', __name__) # init the blueprint for parties module