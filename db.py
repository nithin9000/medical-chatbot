from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["hospital_dbtest"]
hospitals_col = db["hospitals"]

'''from pymongo import MongoClient
import os

#load_dotenv()

MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017/")
client = MongoClient("MONGO_URI")

client = MongoClient("mongodb://localhost:27017/")
db = client["hospital_dbtest"]
hospitals_col = db["hospitals"]'''