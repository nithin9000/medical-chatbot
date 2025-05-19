from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from doctor_utils import find_specialist_doctors
from model.llm import generate_response
import random

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    message = req.message.strip().lower()

    if " in " in message:
        try:
            specialist, city = map(str.strip, message.split(" in ", 1))
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
