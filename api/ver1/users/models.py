""" contains all the extra models """
from api.strings import id_key
from api.ver1.offices.strings import office_key
from api.ver1.ballot.strings import candidate_key
from api.ver1.parties.strings import party_key
from .strings import *

users = [{ id_key : 1, fname : 'john', lname : 'doe', email: 'johndoe@andela.com', phone: '+254 713 972 278', pspt : 'passport.jpg', admin: False}, { id_key : 2, fname : 'maina', lname : 'maenor', email: 'maenor@slack.fr', phone: '+254 782 632 854', pspt : 'pass2.png', admin: False}]

candidates = [{ id_key: 1, office_key: 3, party_key: 1, candidate_key: 1}, {id_key: 2, office_key: 3, party_key: 2, candidate_key: 2}, {id_key: 3, office_key: 2, party_key: 3, candidate_key: 3 }]
