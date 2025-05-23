from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from doctor_utils import find_specialist_doctors
from model.llm import generate_response
import random
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

def parse_appointment_request(message):
    # Example pattern for booking:
    # "book appointment with Dr. Meena Kumar on 2025-05-23 at 10:30 AM. My name is Avathika Rajesh and phone is 9876543210"
    pattern = re.compile(
        r"book appointment with (dr\.? [a-z\s]+) on (\d{4}-\d{2}-\d{2}) at ([0-9:apm\s]+)\.?\s*my name is ([a-z\s]+) and phone is (\d+)", 
        re.IGNORECASE)
    
    match = pattern.search(message)
    if match:
        doctor = match.group(1).title()
        date = match.group(2)
        time = match.group(3).strip()
        patient_name = match.group(4).title()
        phone = match.group(5)
        return doctor, date, time, patient_name, phone
    return None

@app.post("/chat")
async def chat(req: ChatRequest):
    message = req.message.strip()

    # Check for booking request with patient details
    booking_info = parse_appointment_request(message)
    if booking_info:
        doctor, date, time, patient_name, phone = booking_info
        response = (
            f"<strong>Appointment booked successfully!</strong><br><br>"
            f"👤 <strong>Patient:</strong> {patient_name}<br>"
            f"📞 <strong>Phone:</strong> {phone}<br>"
            f"🩺 <strong>Doctor:</strong> {doctor}<br>"
            f"📅 <strong>Date:</strong> {date}<br>"
            f"⏰ <strong>Time:</strong> {time}<br><br>"
            f"📍 Please arrive 15 minutes early. You will also receive a confirmation email."
        )
        return {"response": response}

    # Existing doctor search logic
    if " in " in message.lower():
        try:
            specialist, city = map(str.strip, message.lower().split(" in ", 1))
            doctors = find_specialist_doctors(city, specialist)
            if doctors:
                response = f"<strong>Here are some {specialist.title()}s in {city.title()}:</strong><br>"
                selected_doctors = random.sample(doctors, min(len(doctors), 10))
                for doc in selected_doctors:
                    link = doc['maps_link']
                    response += (
                        f"<div style='margin-bottom: 10px;'>"
                        f"🩺 <strong>{doc['name']}</strong> — {doc['designation']}<br>"
                        f"🏥 {doc['hospital']} ({doc['location']})<br>"
                        f"<a href='{link}' target='_blank' rel='noopener noreferrer'>📍 View on Google Maps</a>"
                        f"</div>"
                    )
            else:
                response = f"❌ Sorry, no {specialist.title()}s found in {city.title()}."
        except Exception as e:
            response = f"⚠️ Doctor lookup failed: {str(e)}"
    else:
        try:
            response = generate_response(message)
        except Exception as e:
            response = f"❌ LLM Error: {str(e)}"

    return {"response": response}
