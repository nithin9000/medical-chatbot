from fastapi import FastAPI, Request, Form
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
        })

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