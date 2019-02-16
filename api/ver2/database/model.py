import psycopg2
from instance.config import app_config
from werkzeug.security import generate_password_hash
from psycopg2.extras import RealDictCursor
from api.ver2.database import create_table_queries, table_names


class Database:
    """ The class model for executing DB transactions """
    def __init__(self, config):
        self.config = config

    def connect(self):
        database_url = app_config[self.config].DATABASE_URL
        print(database_url)
        try:
            global connection, cursor
            connection = psycopg2.connect(database_url)
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            return True
        except Exception as error:
            print('Error. Unable to establish Database connection')
            print(error)
            return False

    def create_db_tables(self):
        print(cursor)
        for query in create_table_queries:
            cursor.execute(query)
        connection.commit()

    def drop_db_tables(self):
        for table in table_names:
            cursor.execute('DROP TABLE IF EXISTS {} CASCADE'.format(table))
        connection.commit()

    def create_root_user(self):
        query = "SELECT * FROM politico_auth WHERE email = 'w.gichuhi5@students.ku.ac.ke'"
        cursor.execute(query)
        user = cursor.fetchone()

        if not user:
            cursor.execute(
                "INSERT INTO politico_auth (email, password, admin) "
                "VALUES ('w.gichuhi5@students.ku.ac.ke', '{}', True)"
                    .format(generate_password_hash('kadanieet')))
            connection.commit()

    def insert(self, query):
        cursor.execute(query)
        data = cursor.fetchone()
        connection.commit()
        print(data)
        return data

    def fetch_one(self, query):
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        return data

    def fetch_all(self, query):
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def execute(self, query):
        cursor.execute(query)
        connection.commit()

    def truncate(self):
        cursor.execute('TRUNCATE TABLE ' + ','.join(table_names) + ' CASCADE')
        connection.commit()
