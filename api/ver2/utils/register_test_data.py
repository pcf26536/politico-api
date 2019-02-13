from api.ver1.ballot.models import candidates
from api.strings import id_key
from api.ver1.ballot.strings import candidate_key
from api.ver1.offices.strings import office_key
from api.ver1.parties.strings import party_key


correct_candidate_infor = candidates[0]
del correct_candidate_infor[id_key]

candidate_id_unexisting_infor = correct_candidate_infor
candidate_id_unexisting_infor[candidate_key] = 100000000

office_id_unexisting_info = correct_candidate_infor
office_id_unexisting_info[office_key] = 100000

party_id_unexisting_info = correct_candidate_infor
party_id_unexisting_info[party_key] = 1000000
