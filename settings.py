import os

from dotenv import load_dotenv, dotenv_values

load_dotenv()


MYSQL_BIDDING = {
    "DATABASE": os.getenv("DB_DATABASE"),
    "HOST": os.getenv("DB_HOST"),
    "USER": os.getenv("DB_USERNAME"),
    "PASSWORD": os.getenv("DB_PASSWORD"),
    "PORT": os.getenv("DB_PORT"),
}

PYMYSQL_URL = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'.format(**MYSQL_BIDDING)

# MYSQL_BIDDING = {
#     "NAME": "bidding",
#     "HOST": "120.78.129.201",
#     "USER": "bidding_select",
#     "PASSWORD": "qweqwe123",
#     "PORT": 3306,
# }

MONGO_BIDDING = {
    "HOST": "localhost",
    "USER": "root",
    "PASSWORD": "example",
    "PORT": 27017,
}

MONGO_URL = 'mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/'.format(**MONGO_BIDDING)
