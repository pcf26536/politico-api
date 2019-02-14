from api.ver2.database.model import Database
from api.strings import status_200
import os


class Skeleton(Database):
    """ the skeleton model """
    def __init__(self, entity, table):
        super().__init__(os.getenv('APP_SETTINGS'))
        self.table = table
        self.entity = entity
        self.message = ""
        self.code = status_200

    def to_json(self):
        pass

    def from_json(self, json):
        return self

    def validate_self(self):
        """ validates an object """
        return True

    def params_to_values(self, params):
        f = ["'{}'".format(i) for i in params]
        return ", ".join(f)

    def add(self, fields, *values):
        """ insert a row to table """
        query = "INSERT INTO {} ({}) \
        VALUES ({}) RETURNING *".format(
            self.table, fields, self.params_to_values(values)
        )
        print(query)
        return super().insert(query)

    def patch(self, key, value, id):
        """ patches a column of a table """

        query = "UPDATE {} SET {} = '{}' WHERE id = '{}' \
            RETURNING *".format(self.table, key, value, id)
        return self.insert(query)

    def get_all(self):
        """  fetches all items in a table """
        query = "SELECT * FROM {}".format(self.table)
        return self.fetch_all(query)

    def delete(self, id):
        """ deletes an item from a table """
        query = "DELETE FROM {} WHERE id = {}".format(self.table, id)
        self.execute(query)

    def get_by(self, key, value):
        """ search for a row in a table """
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        return self.fetch_one(query)
