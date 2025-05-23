from db import hospitals_col
import re

SPECIALIST_SYNONYMS = {
    "cardiologist": "cardiology",
    "heart doctor": "cardiology",
    "heart": "cardiology",
    "skin specialist": "dermatology",
    "dermatologist": "dermatology",
    "oncologist": "oncology",
    "cancer": "oncology",
    "diabetes": "endocrinology",
    "endocrinologist": "endocrinology",
    "ent": "ent",
    "ear nose throat": "ent",
    "nutritionist": "nutrition",
    "dietician": "nutrition",
    "fertility": "fertility",
    "dentist": "dental",
    "pediatrician": "pediatrics",
    "speech therapist": "pediatrics",
    "gynaecologist": "Obstetrics and Gynecology",
    "gyna": "Obstetrics and Gynecology",
    "physician": "General Physician",
    "General Practitioner":"General Physician"

}

def extract_specialist(message:str):
    pattern = r"(.*?)\s+in\s+([a-zA-Z\s]+)$"
    match = re.search(pattern,message.strip().lower())
    if match:
        return match.group(1).strip().match.group(2).strip()
    return None,None

def find_specialist_doctors(city, specialist):
    results = []

    specialist = SPECIALIST_SYNONYMS.get(specialist.lower(), specialist)

    hospitals = hospitals_col.find({ "address.city": {"$regex": city, "$options": "i"} })

    for hospital in hospitals:
        for dept in hospital.get("departments", []):
            dept_name = dept.get("name") or dept.get("dept_name") or ""
            if specialist.lower() in dept_name.lower():
                for doctor in dept.get("doctors", []):
                    coords = hospital.get("coordinates", {})
                    lat, lng = coords.get("latitude"), coords.get("longitude")

                    maps_link = (
                        f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
                        if lat and lng else None
                    )

                    results.append({
                        "name": doctor.get("name", "Unknown"),
                        "designation": doctor.get("designation", "Unknown"),
                        "hospital": hospital.get("hospital_name", "Unknown"),
                        "location": f"{hospital['address'].get('city', '')}, {hospital['address'].get('state', '')}",
                        "maps_link": maps_link
                    })

    return results
