from pymongo import Connection
from os import environ

MONGOHQ_USERNAME = environ["MONGOHQ_USERNAME"]
MONGOHQ_PASSWORD = environ["MONGOHQ_PASSWORD"]
MONGOHQ_PORT = environ["MONGOHQ_PORT"]
MONGOHQ_DATABASE = environ["MONGOHQ_DATABASE"]

MONGOHQ_URI = "mongodb://%s:%s@staff.mongohq.com:%s/%s" % \
              (MONGOHQ_USERNAME, MONGOHQ_PASSWORD, \
               MONGOHQ_PORT, MONGOHQ_DATABASE)

def connect_db():
	return Connection(MONGOHQ_URI)[MONGOHQ_DATABASE]
