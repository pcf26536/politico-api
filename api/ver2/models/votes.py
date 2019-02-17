from .skeleton import Skeleton
from .users import User
from .offices import Office
from .candidates import Candidate
from api.strings import id_key, status_400, status_404, status_409
from api.ver1.offices.strings import office_key
from api.ver1.ballot.strings import candidate_key, createdBy_key, createdOn_key
from api.ver2.utils.validators import is_int, valid_date, no_date_diff


class Vote(Skeleton):
    def __init__(self, created_on=None, created_by=None, office_id=None, candidate_id=None):
        super().__init__('Vote', 'politico_votes')

        self.created_on = created_on
        self.created_by = created_by
        self.office = office_id
        self.candidate = candidate_id
        self.Id = None

    def create(self):
        data = super().add(
            createdOn_key + ',' + createdBy_key + ', ' + office_key + ', ' + candidate_key,
            self.created_on, self.created_by, self.office, self.candidate
        )
        self.Id = data.get(id_key)
        return data

    def to_json(self):
        # get the object as a json
        return {
            id_key: self.Id,
            createdOn_key: self.created_on,
            createdBy_key: self.created_by,
            office_key: self.office,
            candidate_key: self.candidate
        }

    def from_json(self, json):
        self.__init__(
            json[createdOn_key],
            json[createdBy_key],
            json[office_key],
            json[candidate_key])
        self.Id = json[id_key]
        return self

    def validate_vote(self):
        if not is_int(self.created_by):
            self.message = "String types are not allowed for Created By field"
            self.code = status_400
            return False

        if not is_int(self.candidate):
            self.message = "String types are not allowed for Candidate ID field"
            self.code = status_400
            return False

        if not is_int(self.office):
            self.message = "String types are not allowed for Office ID field"
            self.code = status_400
            return False

        if not User().get_by(id_key, self.created_by):
            self.message = 'Selected User does not exist'
            self.code = status_404
            return False

        if not Office().get_by(id_key, self.office):
            self.message = 'Selected Office does not exist'
            self.code = status_404
            return False

        if not Candidate().get_by(candidate_key, self.candidate):
            self.message = "Selected Candidate does not exist"
            self.code = status_404
            return False

        if self.get_by(createdBy_key, self.created_by) and self.get_by(office_key, self.office):
            self.message = 'User has already voted for specified office'
            self.code = status_409
            return False

        if not valid_date(self.created_on):
            self.message = "Invalid date format; expected format is YYYY-MM-DD e.g 2019-12-30"
            self.code = status_400
            return False

        if not no_date_diff(self.created_on):
            self.message = "The date entered doesn't match today's date"
            self.code = status_400
            return False

        return super().validate_self()


