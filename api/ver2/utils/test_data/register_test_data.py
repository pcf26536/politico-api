from api.ver1.ballot.models import candidates
from api.strings import id_key
from api.ver1.ballot.strings import candidate_key
from api.ver1.offices.strings import office_key
from api.ver1.parties.strings import party_key


correct_candidate_infor = candidates[0]
del correct_candidate_infor[id_key]
del correct_candidate_infor['office']

correct_candidate_infor_2 = candidates[1]
del correct_candidate_infor_2[id_key]
del correct_candidate_infor_2['office']

candidate_id_unexisting_infor = correct_candidate_infor.copy()
candidate_id_unexisting_infor[candidate_key] = 100000000

party_id_unexisting_info = correct_candidate_infor.copy()
party_id_unexisting_info[party_key] = 1000000
