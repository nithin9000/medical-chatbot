from db import hospitals_col

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
    "gynaecologist":"Obstetrics and Gynecology",
    "gyna":"Obstetrics and Gynecology"
}

def find_specialist_doctors(city, specialist):
    results = []


    specialist_key = specialist.lower().strip()
    mapped_specialist = SPECIALIST_SYNONYMS.get(specialist_key, specialist_key)

    hospitals = hospitals_col.find({ "address.city": {"$regex": city, "$options": "i"} })

    for hospital in hospitals:
        for dept in hospital.get("departments", []):
            dept_name = (dept.get("name") or dept.get("dept_name") or "").lower()

            if mapped_specialist in dept_name or dept_name in mapped_specialist:
                for doctor in dept.get("doctors", []):
                    results.append({
                        "name": doctor.get("name", "Unknown"),
                        "designation": doctor.get("designation", "Unknown"),
                        "hospital": hospital.get("hospital_name", "Unknown"),
                        "location": f"{hospital['address'].get('city', '')}, {hospital['address'].get('state', '')}"
                    })

    return results

'''
def find_specialist_doctors(city, specialist):
    results = []

    # Normalize specialist input
    specialist_key = specialist.lower().strip()
    mapped_specialist = SPECIALIST_SYNONYMS.get(specialist_key, specialist_key)

    hospitals = hospitals_col.find({ "address.city": {"$regex": city, "$options": "i"} })

    for hospital in hospitals:
        for dept in hospital.get("departments", []):
            dept_name = dept.get("name") or dept.get("dept_name") or ""

            if mapped_specialist in dept_name.lower():
                for doctor in dept.get("doctors", []):
                    results.append({
                        "name": doctor.get("name", "Unknown"),
                        "designation": doctor.get("designation", "Unknown"),
                        "hospital": hospital.get("hospital_name", "Unknown"),
                        "location": f"{hospital['address'].get('city', '')}, {hospital['address'].get('state', '')}"
                    })

    return results'''