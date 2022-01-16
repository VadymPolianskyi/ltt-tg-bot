import os

BOT_API_KEY = os.getenv("BOT_API_KEY")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DB_TABLE_ACTIVITY = os.environ.get("DB_TABLE_ACTIVITY")
DB_TABLE_EVENT = os.environ.get("DB_TABLE_EVENT")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
