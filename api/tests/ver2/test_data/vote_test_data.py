from api.ver1.ballot.models import votes
from api.strings import id_key
from api.ver1.offices.strings import office_key
from api.ver1.ballot.strings import candidate_key, createdBy_key, createdOn_key

correct_vote = votes[0]
del correct_vote[id_key]

office_does_not_exist_vote = correct_vote.copy()
office_does_not_exist_vote[office_key] = 100

candidate_does_not_exist_vote = correct_vote.copy()
candidate_does_not_exist_vote[candidate_key] = 10000

voter_does_not_exist_vote = correct_vote.copy()
voter_does_not_exist_vote[createdBy_key] = 10000

invalid_date_vote = correct_vote.copy()
invalid_date_vote[createdOn_key] = 'fake date'

string_candidate_vote = correct_vote.copy()
string_candidate_vote[candidate_key] = 'fake date'
