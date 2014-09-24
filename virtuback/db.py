"""
Database module for virtuback
"""
from pymongo import MongoClient

MONGOURL = 'mongodb://virtusize:easysizing@37.139.5.104:27017/virtuback'


def collection():
    client = MongoClient(MONGOURL)
    collection = client.virtuback.users
    return collection

