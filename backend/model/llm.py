import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_response(prompt: str) -> str:
    SYSTEM_PROMPT = (
        "You are MedBot, a helpful and professional medical assistant. "
        "You can only answer questions related to medicine, healthcare, diseases, symptoms, treatments, doctors, and wellness. "
        "If the user asks anything outside the medical domain, respond with:\n"
        "'I'm sorry, I can only assist with medical-related queries.'"
    )

    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {prompt}\nMedBot:"

    payload = {
        #"model": "llama3-chatqa:8b",
        "model":"deepseek-r1:14b",
        "prompt": full_prompt,
        "stream": False
    }

    try:
        res = requests.post("http://localhost:11434/api/generate", json=payload)
        res.raise_for_status()
        data = res.json()
        return data.get("response", "").strip()
    except Exception as e:
        return f"❌ Ollama error: {str(e)}"
