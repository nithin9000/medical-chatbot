from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from doctor_utils import find_specialist_doctors,extract_specialist_city,SPECIALIST_SYNONYMS
#from model.llm import generate_response,generate_response_from_context
from model.llm import generate_response
#from model.rag import find_best_response,load_embedding_model
import random

app = FastAPI()

#index,responses,embeddings_model = load_embedding_model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str
    chat_history: str = ""

@app.post("/chat")
async def chat(req: ChatRequest):
    message = req.message.strip()
    history = req.chat_history.strip()

    specialists = list(SPECIALIST_SYNONYMS.keys())+list(SPECIALIST_SYNONYMS.values())
    specialist,city = extract_specialist_city(message,specialists)

    if specialist and city:
        doctors = find_specialist_doctors(city,specialist)
        if doctors:
            response = f"<strong>Here are some {specialist.title()}s in {city.title()}:</strong><br><br>"
            selected_doctors = random.sample(doctors,min(len(doctors),10))
            for doc in selected_doctors:
                link = doc['maps_link']
                response += (
                    f"<div style = 'margin-bottom:10px;'> "
                    f"🩺 <strong>{doc['name']}</strong> — {doc['designation']}<br>"
                    f"🏥 {doc['hospital']} ({doc['location']})<br>"
                    f"<a href='{link}' target='_blank' rel='noopener noreferrer'>📍 View on Google Maps</a>"
                    f"</div>"
                )
        else:
            response = f"❌ Sorry, no {specialist.title()}s found in {city.title()}"
            '''else:
                response = "⚠️ Sorry, I couldn't understand the specialist and city"'''

            '''
            if " in " in message.lower():
                try:
                    specialist, city = map(str.strip, message.split(" in ", 1))
                    doctors = find_specialist_doctors(city, specialist)
                    if doctors:
                        response = f"<strong>Here are some {specialist.title()}s in {city.title()}:</strong><br><br>"
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
                    response = f"⚠️ Doctor lookup failed: {str(e)}"'''
    else:
        try:
            llm_response = generate_response(message,chat_history = history)
            ps_note = "\n\n<i>Ps: I'm not a certified doctor. Please verify this information with a certified medical professional.</i>"
            response = llm_response + ps_note
        except Exception as e:
            response = f"❌ LLM Error: {str(e)}"

    return {"response": response}
