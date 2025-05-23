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
    "gynaecologist": "Obstetrics and Gynecology",
    "gyna": "Obstetrics and Gynecology",
    "physician": "General Physician",
    "General Practitioner":"General Physician"

}

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
