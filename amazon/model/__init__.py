from pymongo import MongoClient

client = MongoClient('localhost', port=27017)
db = client['pymlb2-amazon']