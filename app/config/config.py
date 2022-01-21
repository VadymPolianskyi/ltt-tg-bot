import os

SERVER_HOST = os.environ.get('HOST', "0.0.0.0")
SERVER_PORT = int(os.environ.get('PORT', 5000))

BOT_API_KEY = os.getenv("BOT_API_KEY")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_TABLE_ACTIVITY = os.getenv("DB_TABLE_ACTIVITY")
DB_TABLE_EVENT = os.getenv("DB_TABLE_EVENT")
DB_TABLE_USER = os.getenv("DB_TABLE_USER")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
