import configparser
import os

config = configparser.ConfigParser()
config.read('app/config/conf.ini')

BOT_API_KEY = os.getenv("BOT_API_KEY")

DB_HOST = config['DB']['Host']
DB_PORT = int(config['DB']['Port'])
DB_NAME = config['DB']['Database']
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DB_TABLE_ACTIVITY = os.environ.get("ACTIVITY_TABLE")
DB_TABLE_EVENT = os.environ.get("EVENT_TABLE")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
