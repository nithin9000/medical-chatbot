import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def build_prompt(chat_history):
    prompt = "<|start_header_id|>system<|end_header_id|>\nYou are MedBot, a helpful and professional medical assistant. "
    "You can only answer questions related to medicine, healthcare, diseases, symptoms, treatments, doctors, and wellness. "
    "If the user asks anything outside the medical domain, respond with:\n"
    "'I'm sorry, I can only assist with medical-related queries.'<|eot_id|> \n\n"
    for msg in chat_history:
        if msg["role"] == "user":
            prompt += "<|start_header_id|>user<|end_header_id|>\n"
            prompt += msg["text"] + "<|eot_id|>\n"
        elif msg["role"] == "bot":
            prompt += "<|start_header_id|>assistant<|end_header_id|>"
            prompt += msg["text"] + "<|eot_id|>\n"

    prompt += "<|start_header_id|>assistant<|end_header|"
    return prompt


def generate_response(chat_history:list[dict]) -> str:
#def generate_response(question:str,context:str) -> str:
    '''SYSTEM_PROMPT = (
        "You are MedBot, a helpful and professional medical assistant. "
        "You can only answer questions related to medicine, healthcare, diseases, symptoms, treatments, doctors, and wellness. "
        "If the user asks anything outside the medical domain, respond with:\n"
        "'I'm sorry, I can only assist with medical-related queries.'"
    )
    messages = [
        {"role":"system","context":"You are MedBot, a helpful and professional medical assistant. "
        "You can only answer questions related to medicine, healthcare, diseases, symptoms, treatments, doctors, and wellness. "
        "If the user asks anything outside the medical domain, respond with:\n"
        "'I'm sorry, I can only assist with medical-related queries.'"}
    ] + chat_history'''

    #full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {prompt}\nMedBot:"
    #full_prompt = build_prompt(chat_history)
    prompt = build_prompt(chat_history)
    payload = {
        #"model": "llama3-chatqa:8b",
        "model":"llava-llama3:8b",
        "prompt": prompt,
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload)
        res.raise_for_status()
        data = res.json()
        return data.get("response", "").strip()
    except Exception as e:
        return f"❌ Ollama error: {str(e)}"

