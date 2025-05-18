from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["hospital_dbtest"]
hospitals_col = db["hospitals"]