import requests
from bs4 import BeautifulSoup
import json
import pymongo

# Generate unique ID
def generate_id(prefix):
    from uuid import uuid4
    return f"{prefix}_{uuid4().hex[:8]}"

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["hospital_dbtest"]
collection = db["hospitals123"]

# Website URL
URL = "https://www.kimshealth.org/trivandrum/doctors/"
headers = {"User-Agent": "Mozilla/5.0"}

# Fetch the webpage
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Hospital information
hospital_data = {
    "hospital_id": generate_id("hosp"),
    "hospital_name": "KIMSHEALTH Trivandrum",
    "address": {
        "street": "P.B. No.1, Anayara P.O.",
        "city": "Thiruvananthapuram",
        "district": "Thiruvananthapuram",
        "state": "Kerala",
        "pin": "695029"
    },
    "contact": {
        "phone": "+91 471 294 1101",
        "email": "info@kimshealth.org",
        "website": URL
    },
    "departments": []
}

# Scrape doctor details
doctor_cards = soup.find_all("div", class_="doctor-card")

departments = {}

for card in doctor_cards:
    name = card.find("h3").text.strip()
    designation = card.find("p").text.strip()
    dept_name = card.find("h4").text.strip()  # Assuming department is mentioned

    # Extract appointment timings (Modify if structure differs)
    appointment_info = []
    if card.find("ul", class_="appointment-times"):
        for time_slot in card.find_all("li"):
            day, times = time_slot.text.split(":")
            appointment_info.append({
                "day": day.strip(),
                "timings": [t.strip() for t in times.split(",")]
            })

    # Add to department dictionary
    if dept_name not in departments:
        departments[dept_name] = {
            "dept_id": generate_id("dept"),
            "name": dept_name,
            "doctors": []
        }

    # Append doctor details
    departments[dept_name]["doctors"].append({
        "doctor_id": generate_id("doc"),
        "name": name,
        "designation": designation,
        "appointments": appointment_info if appointment_info else None
    })

# Add departments to hospital data
hospital_data["departments"] = list(departments.values())

# Insert data into MongoDB
collection.insert_one(hospital_data)

# Print JSON output
print(json.dumps(hospital_data, indent=4))