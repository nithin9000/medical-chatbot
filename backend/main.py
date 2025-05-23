from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import random
import re

from doctor_utils import find_specialist_doctors
from model.llm import generate_response  # LLaVA-compatible
# Note: chat_histories stores past messages

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_histories = {}

class ChatRequest(BaseModel):
    message: str
    chat_id: str = None

def extract_specialist_and_city(message: str):
    # Looser match — allows trailing punctuation
    pattern = r"(.*?)\s+in\s+([a-zA-Z\s]+)[\?\.!]*$"
    match = re.search(pattern, message.strip().lower())
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None, None

@app.post("/chat")
async def chat(req: ChatRequest):
    message = req.message.strip()
    chat_id = req.chat_id or str(uuid4())

    if chat_id not in chat_histories:
        chat_histories[chat_id] = []

    # 👨‍⚕️ Attempt doctor query detection
    specialist, city = extract_specialist_and_city(message)
    print(f"🧪 Extracted => Specialist: '{specialist}', City: '{city}'")

    if specialist and city:
        try:
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
                return {"response": response, "chat_id": chat_id}
            else:
                return {
                    "response": f"❌ Sorry, no {specialist.title()}s found in {city.title()}.",
                    "chat_id": chat_id
                }
        except Exception as e:
            return {
                "response": f"⚠️ Doctor lookup failed: {str(e)}",
                "chat_id": chat_id
            }

    # 🧠 Otherwise, pass to LLM with chat history
    chat_histories[chat_id].append({"role": "user", "text": message})

    try:
        llm_reply = generate_response(chat_histories[chat_id])
        chat_histories[chat_id].append({"role": "bot", "text": llm_reply})
        final_response = llm_reply + "\n\nPs: I'm not a certified doctor. Please verify this information with a certified medical professional."
    except Exception as e:
        final_response = f"❌ LLM Error: {str(e)}"

    return {"response": final_response, "chat_id": chat_id}