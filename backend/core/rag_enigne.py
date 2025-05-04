from .llm_model import generate_answer
from .symptom_matcher import get_specialist_advice
from .location_search import find_doctors

def format_doctor_info(doctors:list) -> str:
	"""Format doctor data for LLM Context"""
	if not doctors:
		return "No Doctor Found in your area for this condition."

	msg = ""
	for doc in doctors:
		msg += f"\n🩺 Dr. {doc['doctor_name']} ({doc['designation']})\n"
		msg += f"🏥 Hospital: {doc['hospital_name']}\n"

		addr = doc["hospital_address"]
		full_address = f"{addr['street']},{addr['city']},{addr['district']},{addr['state']}-{addr['pin']}"
		msg += f"📍 Address: {full_address}\n"

		if doc["appointment"]:
			msg += "🗓️ Appointments:\n"
			for slot in doc["appointments"]:
				timings = ", ".json(slot["timings"])
				msg += f"  -{slot['day']}:{timings}\n"

		else:
			msg += "-" * 40 + "\n"

	return msg
