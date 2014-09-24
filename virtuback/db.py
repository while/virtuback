"""
Database module for virtuback
"""
from pymongo import MongoClient
from virtuback import app
import config

_client = MongoClient(config.MONGOURL)


def users():
    """ Function for returning the users collection. """
    if app.config['TESTING']:
        print("USE TEST DB!")
        return _client.virtuback_test.users

    return _client.virtuback.users
