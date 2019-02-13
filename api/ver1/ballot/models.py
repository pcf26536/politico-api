from api.strings import id_key
from .strings import *
from api.ver1.offices.strings import office_key
from api.ver1.parties.strings import party_key

votes = [
    { id_key: 1, createdOn_key: '11/11/18', createdBy_key: 1, office_key: 2, candidate_key: 1 },
    { id_key: 2, createdOn_key: '11/11/18', createdBy_key: 1, office_key: 1, candidate_key: 2 }
]

petitions = [
    { id_key: 1, createdOn_key: '01/01/19', createdBy_key: 1, office_key: 2, body_key: 'The voting was rigged!!'},
    { id_key: 2, createdOn_key: '20/01/19', createdBy_key: 3, office_key: 2, body_key: 'Vifaranga wa compyuta!'}
]

candidates = [
    {id_key: 1, office_key: 1, party_key: 1, candidate_key: 1},
    {id_key: 2, office_key: 1, party_key: 2, candidate_key: 2},
    {id_key: 3, office_key: 1, party_key: 3, candidate_key: 3},
    {id_key: 4, office_key: 2, party_key: 1, candidate_key: 4},
    {id_key: 5, office_key: 2, party_key: 2, candidate_key: 5}
]