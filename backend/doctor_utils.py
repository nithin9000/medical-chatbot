from db import hospitals_col
import re
from rapidfuzz import fuzz


GREETING_KEYWORDS = [
    "hey","hello","hi","sup","yo","hai","hola",
]

known_specialists = [
    "cardiology", "neurology", "oncology", "orthopedics", "dermatology",
    "endocrinology", "ent", "nutrition", "fertility", "dental",
    "pediatrics", "Obstetrics and Gynecology", "general physician"
]

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
    "General Practitioner":"General Physician",
    "primary care physician":"General Physician",
    "neurologist":"Neurology"

}

def extract_specialist_city(message:str,known_specialist:list,threshold=80):
    message = message.lower()
    match = re.search(r"(.*?)(?:\s+(?:in|at|from)\s+)(.+)",message)
    if not match:
        return None,None
    raw_specialist,raw_city = match.group(1).strip(),match.group(2).strip()

    best_match = max(
        known_specialists,
        key = lambda sp: fuzz.partial_ratio(sp.lower(),raw_specialist.lower()),
        default = None
    )
    if fuzz.partial_ratio(best_match.lower(),raw_specialist.lower()) >= threshold:
        return best_match,raw_city
    return None,raw_city


def find_specialist_doctors(city, specialist):
    results = []

    specialist = SPECIALIST_SYNONYMS.get(specialist.lower(), specialist)

    hospitals = hospitals_col.find({ "address.city": {"$regex": city, "$options": "i"} })

    for hospital in hospitals:
        for dept in hospital.get("departments", []):
            dept_name = dept.get("name") or dept.get("dept_name") or ""
            if specialist.lower() in dept_name.lower():
                for doctor in dept.get("doctors", []):
                    hospital_name = hospital.get("hospital_name", "")
                    hospital_city = hospital.get("address", {}).get("city", "")
                    search_query = f"{hospital_name} {hospital_city}".replace(" ", "+")

                    maps_link = f"https://www.google.com/maps/search/?api=1&query={search_query}"


                    results.append({
                        "name": doctor.get("name", "Unknown"),
                        "designation": doctor.get("designation", "Unknown"),
                        "hospital": hospital.get("hospital_name", "Unknown"),
                        "location": f"{hospital['address'].get('city', '')}, {hospital['address'].get('state', '')}",
                        "maps_link": maps_link
                    })

    return results
