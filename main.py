from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from doctor_utils import find_specialist_doctors

app = FastAPI()

# Allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with frontend URL in prod
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message
    if " in " not in message.lower():
        return {"response": "🧠 Please ask like: `cardiologist in delhi`"}

    try:
        specialist, city = map(str.strip, message.lower().split(" in ", 1))
        doctors = find_specialist_doctors(city, specialist)
        if doctors:
            response = f"Here are some {specialist.title()}s in {city.title()}:\n"
            for doc in doctors[:5]:
                response += (
                    f"\n🩺 {doc['name']} — {doc['designation']} "
                    f"at {doc['hospital']} ({doc['location']})"
                )
        else:
            response = f"❌ Sorry, I couldn’t find any {specialist.title()}s in {city.title()}."
    except Exception:
        response = "⚠️ Please use the format: `specialist in city`."

    return {"response": response}
'''from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from doctor_utils import find_specialist_doctors

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 🧠 In-memory chat history (clears on server restart)
chat_history = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "history": chat_history
    })

@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    # Store user message
    chat_history.append({"role": "user", "text": message})

    response = ""  # bot response

    # Very basic parsing: expecting "specialist in city"
    if " in " in message.lower():
        try:
            specialist, city = map(str.strip, message.lower().split(" in ", 1))
            doctors = find_specialist_doctors(city, specialist)

            if doctors:
                response = f"Here are some {specialist.title()}s in {city.title()}:\n"
                for doc in doctors[:5]:  # limit to 5 results
                    response += (
                        f"\n🩺 {doc['name']} — {doc['designation']} "
                        f"at {doc['hospital']} ({doc['location']})"
                    )
            else:
                response = f"❌ Sorry, I couldn’t find any {specialist.title()}s in {city.title()}."
        except Exception:
            response = "⚠️ Please use the format: `specialist in city`."
    else:
        response = "🧠 Please ask like: `cardiologist in delhi` or `dentist in mumbai`."

    # Store bot response
    chat_history.append({"role": "bot", "text": response})

    return templates.TemplateResponse("index.html", {
        "request": request,
        "history": chat_history
    })'''

'''from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from doctor_utils import find_specialist_doctors

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def search_doctors(request: Request):
    try:
        form = await request.form()
        city = form.get("city", "").strip()
        specialist = form.get("specialist", "").strip()

        if not city or not specialist:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": "Please enter both city and specialist."
            })

        doctors = find_specialist_doctors(city, specialist)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "doctors": doctors,
            "city": city,
            "specialist": specialist
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Something went wrong: {str(e)}"
        })'''
'''from doctor_utils import find_specialist_doctors

def chatbot():
    print("🩺 Welcome to MedBot!")
    print("Type 'exit' anytime to quit.\n")

    while True:
        city = input("Enter your city: ").strip()
        if city.lower() == "exit":
            break

        specialist = input("Enter the specialist you need (e.g. Cardiologist): ").strip()
        if specialist.lower() == "exit":
            break

        doctors = find_specialist_doctors(city, specialist)

        if not doctors:
            print("❌ No matching doctors found.\n")
        else:
            print(f"\n✅ Found {len(doctors)} doctor(s):\n")
            for i, doc in enumerate(doctors, 1):
                print(f"{i}. {doc['name']} ({doc['designation']})")
                print(f"   Hospital: {doc['hospital']}")
                print(f"   Location: {doc['location']}\n")

if __name__ == "__main__":
    chatbot()'''