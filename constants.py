from credentials import (
    DB_PASS,
    DB_USER
)

DB_PORT = '3306'
DB_HOST = 'localhost'
DB_NAME = 'task_database'

# construct final URL for sqlalchemy session
DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
