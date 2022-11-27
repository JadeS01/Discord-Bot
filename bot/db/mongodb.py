import pymongo
import os

def get_db():
    mongo_client = pymongo.MongoClient(os.getenv('MONGO_URL'))
    return mongo_client.user_messages

if __name__ == '__mongodb__':
    db = get_db()