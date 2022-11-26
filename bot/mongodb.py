import pymongo
import os

mongo_client = pymongo.MongoClient(os.getenv('MONGO_URL'))
db = mongo_client.user_messages