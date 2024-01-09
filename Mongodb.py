import pymongo
from pymongo import MongoClient
import os

url = os.getenv('url')
cluster = MongoClient(url)
db = cluster["post"]
collection = db["col"]


test = collection.update_one({"name": "doge"}, {"$inc": {"score": 1}})
print("updated")
print(collection.find({"name": "doge"}))


