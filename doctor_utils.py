from db import hospitals_col

# Manual synonym-to-department mapper
SPECIALIST_SYNONYMS = {
    "cardiologist": "cardiology",
    "heart doctor": "cardiology",
    "heart": "cardiology",
    "skin specialist": "dermatology and cosmetology",
    "dermatologist": "dermatology and cosmetology",
    "oncologist": "cancer care",
    "cancer": "cancer care",
    "diabetes": "endorcinology and diabetes",
    "endocrinologist": "endorcinology and diabetes",
    "ent": "ent",
    "ear nose throat": "ent",
    "nutritionist": "clinical nutrition",
    "dietician": "clinical nutrition",
    "fertility": "fertility clinic",
    "dentist": "dental",
    "pediatrician": "development pediatrics",
    "speech therapist": "development pediatrics"
}

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

    return results