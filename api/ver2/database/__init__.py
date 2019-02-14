""" Tables and Queries """

table_names = [
    'politico_users',
    'politico_auth',
    'politico_parties',
    'politico_offices',
    'politico_candidates',
    'politico_votes'
    'politico_petitions'
]

create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS politico_auth(
        id SERIAL PRIMARY KEY NOT NULL,
        email VARCHAR(250) NOT NULL,
        password VARCHAR(250) NOT NULL,
        admin BOOLEAN NOT NULL DEFAULT FALSE,
        UNIQUE(email)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS politico_users(
        user_id INTEGER PRIMARY KEY NOT NULL,
        fname VARCHAR(250) NOT NULL,
        lname VARCHAR(250) NOT NULL,
        phone VARCHAR(250) NULL,
        UNIQUE(phone, user_id)
        FOREIGN KEY (user_id) REFERENCES politico_auth(id) ON DELETE CASCADE,
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS politico_parties(
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(250) NOT NULL,
        hq_address VARCHAR(250) NOT NULL,
        logo_url VARCHAR(250) NULL,
        UNIQUE(name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS politico_offices(
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(250) NOT NULL,
        type VARCHAR(250) NOT NULL,
        UNIQUE(name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS politico_candidates(
        id SERIAL NOT NULL,
        candidate INTEGER NOT NULL DEFAULT 0,
        party INTEGER NOT NULL DEFAULT 0,
        office INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (candidate, office),
        UNIQUE(candidate),
        FOREIGN KEY (candidate) REFERENCES politico_users(id) ON DELETE CASCADE,
        FOREIGN KEY (party) REFERENCES politico_parties(id) ON DELETE CASCADE,
        FOREIGN KEY (office) REFERENCES politico_offices(id) ON DELETE CASCADE,
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS politico_votes(
        id SERIAL NOT NULL,
        office INTEGER NOT NULL DEFAULT 0,
        candidate INTEGER NOT NULL DEFAULT 0,
        createdBy INTEGER NOT NULL DEFAULT 0,
        createdOn  TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        PRIMARY KEY (createdBy, office),
        FOREIGN KEY (office) REFERENCES politico_offices(id) ON DELETE CASCADE,
        FOREIGN KEY (candidate) REFERENCES politico_candidates(candidate) ON DELETE CASCADE,
        FOREIGN KEY (createdBy) REFERENCES politico_users(id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS politico_petitions(
        id SERIAL NOT NULL,
        text VARCHAR(500) NOT NULL,
        evidence VARCHAR(500) NOT NULL,
        office INTEGER NOT NULL DEFAULT 0,
        createdBy INTEGER NOT NULL DEFAULT 0,
        createdOn  TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        PRIMARY KEY (createdBy, office),
        FOREIGN KEY (createdBy) REFERENCES politico_users(id) ON DELETE CASCADE,
        FOREIGN KEY (office) REFERENCES politico_offices(id) ON DELETE CASCADE
    )
    """
]
