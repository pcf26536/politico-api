from api.strings import id_key
from .strings import *
from api.ver1.offices.strings import office_key
from api.ver1.parties.strings import party_key
import datetime

votes = [
    { id_key: 1,
      createdOn_key: datetime.datetime.now().date().__str__()[2:],
      createdBy_key: 2,
      office_key: 1,
      candidate_key: 2
    },
    { id_key: 2,
      createdOn_key: datetime.datetime.now().date().__str__()[2:],
      createdBy_key: 2,
      office_key: 1,
      candidate_key: 2
    }
]

petitions = [
    { id_key: 1,
      createdOn_key: datetime.datetime.now().date().__str__()[2:],
      createdBy_key: 2,
      office_key: 1,
      body_key: 'The voting was rigged!!'
    },
    { id_key: 2,
      createdOn_key: datetime.datetime.now().date().__str__()[2:],
      createdBy_key: 3,
      office_key: 2,
      body_key: 'Vifaranga wa compyuta!'
      }
]

candidates = [
    {id_key: 1, office_key: 1, party_key: 1, candidate_key: 2},
    {id_key: 2, office_key: 1, party_key: 2, candidate_key: 3},
    {id_key: 3, office_key: 1, party_key: 3, candidate_key: 4},
    {id_key: 4, office_key: 2, party_key: 1, candidate_key: 5},
    {id_key: 5, office_key: 2, party_key: 2, candidate_key: 6}
]