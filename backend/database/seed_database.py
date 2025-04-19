import json
from db_connection import hospital_collection

with open("nithin_hospitals.json", "r") as file:
    data = json.load(file)
    hospital_collection.insert_many(data)

print("Database seeded successfully!")