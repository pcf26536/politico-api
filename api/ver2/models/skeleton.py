from api.ver2.database.model import Database
from api.strings import status_200
import os


class Skeleton(Database):
    """ the skeleton model """
    def __init__(self, entity, table):
        super().__init__(os.getenv('APP_SETTINGS'))
        self.table = table
        self.entity = entity
        self.message = ''
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
        return super().insert(query)

    def get_all(self):
        """  fetches all items in a table """
        query = "SELECT * FROM {}".format(self.table)
        return super().fetch_all(query)

    def delete(self, Id):
        """ deletes an item from a table """
        query = "DELETE FROM {} WHERE id = {}".format(self.table, Id)
        super().execute(query)

    def get_by(self, key, value):
        """ search for a row in a table """
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        return super().fetch_one(query)

    def get_by_two(self, key1, value1, key2, value2):
        """ search for a row in a table """
        query = "SELECT * FROM {} WHERE {} = '{}' and {} = '{}'".format(
            self.table, key1, value1, key2, value2)
        return super().fetch_one(query)

    def get_group(self, col1, col2, count_col, grp_col1, grp_col2):
        query = "SELECT {}, {}, COUNT ({}) AS result FROM {} GROUP BY {},{}".format(
            col1, col2, count_col, self.table, grp_col1, grp_col2)
        print(query)
        return super().fetch_all(query)
