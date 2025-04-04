from credentials import DB_PASS, DB_USER

DB_PORT = "3306"
DB_HOST = "localhost"
DB_NAME = "task_database"

# construct final URL for sqlalchemy session
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

API_METADATA = {
    "title": "UsersOrdersAPI",
    "tags_metadata": [
        {
            "name": "Users",
            "description": "Operations with users.",
        },
        {
            "name": "Orders",
            "description": "Operations with orders.",
        },
        {
            "name": "Root",
            "description": "Index endpoint when reaching server address"},
    ],
}
