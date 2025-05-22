from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from doctor_utils import find_specialist_doctors,SPECIALIST_SYNONYMS
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

'''
@app.post("/chat")
async def chat(req: ChatRequest):
    message = req.message.strip().lower()

    #if " in " and "{SPECIALIST_SYNONYMS}"in message:
    if " in " in message:
        try:
            specialist, city = map(str.strip, message.split(" in ", 1))
            doctors = find_specialist_doctors(city, specialist)

            if doctors:
                response = f"<strong>Here are some {specialist.title()}s in {city.title()}:</strong><br><br>"
                for doc in doctors[:5]:
                    response += (
                        f"<div style='margin-bottom: 12px;'>"
                        f"🩺 <strong>{doc['name']}</strong> — {doc['designation']}<br>"
                        f"🏥 {doc['hospital']} ({doc['location']})<br>"
                    )
                    if doc['maps_link']:
                        response += f"<a href='{doc['maps_link']}' target='_blank' rel='noopener noreferrer'>📍 View on Google Maps</a><br>"
                    else:
                        response += "<span style='color:gray'>📍 Location unavailable</span><br>"
                    response += "</div>"
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

'''
@app.post("/chat")
async def chat(req: ChatRequest):
    message = req.message.strip().lower()

    if " in " in message:
        try:
            specialist, city = map(str.strip, message.split( " in ", 1))
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
            llm_response = generate_response(message)
            ps_note = "\n\nPs: I'm not a certified doctor. Please verify this information with a certified medical professional."
            final_response = llm_response + ps_note
        except Exception as e:
            final_response = f"❌ LLM Error: {str(e)}"

    return {"response": final_response}
'''
@app.post("/chat_rag")
async def chat_with_rag(req: ChatRequest):
    try:
        question = req.message.strip()
        context = find_best_response(question, embeddings_model, index, responses)
        answer = generate_response_from_context(question, context)
        return {"context": context, "response": answer}
    except Exception as e:
        return {"response": f"❌ RAG Error: {str(e)}"}
'''