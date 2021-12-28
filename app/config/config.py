import configparser

config = configparser.ConfigParser()
config.read('app/config/conf.ini')

BOT_API_KEY = config['BOT']['ApiKey']

DB_HOST = config['DB']['Host']
DB_PORT = int(config['DB']['Port'])
DB_NAME = config['DB']['Database']
DB_USERNAME = config['DB']['Username']
DB_PASSWORD = config['DB']['Password']

DB_TABLE_ACTIVITY = config['TABLE']['Activity']
DB_TABLE_EVENT = config['TABLE']['Event']
