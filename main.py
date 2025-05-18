from doctor_utils import find_specialist_doctors

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
    chatbot()