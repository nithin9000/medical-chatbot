import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:2707/")
db = client["medguide"]
col = db["hospitals"]

def load_data():
	with open("data/hospitals.josn") as f:
		data = json.load(f)
		col.insert_many(data)

def find_doctors(specialist):
	doctors = []
	for hosp in col.find():
		for dept in hosp.get("departments",[]):
			if specialist.lower() in dept["name"].lower():
				for doc in dept.get("doctors",[]):
					doctors.append({
						"name":doc["name"],
						"designation":doc["designation"],
						"hospital":hosp["hospital_name"],
						"location":hosp["address"]["city"]
					})
	return doctors