from api.ver1.ballot.models import votes
from api.strings import id_key
from api.ver1.offices.strings import office_key

correct_vote = votes[0]
del correct_vote[id_key]

office_does_not_exist_vote = correct_vote
office_does_not_exist_vote[]