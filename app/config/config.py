import configparser
import os

config = configparser.ConfigParser()
env = os.environ.get("ENV")

config.read(f'app/config/{env}.ini')

BOT_API_KEY = os.getenv("BOT_API_KEY")

DB_HOST = config['DB']['Host']
DB_PORT = int(config['DB']['Port'])
DB_NAME = config['DB']['Database']
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DB_TABLE_ACTIVITY = config['TABLE']['Activity']
DB_TABLE_EVENT = config['TABLE']['Event']

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
