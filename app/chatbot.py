from app.rag_engine import retrieve_docs
from app.specialist_mapper import get_specialist_openbio
from app.mongo_fetcher import find_doctors
from transformers import AutoModelForCausalLM,AutoTokenizer
import torch

model_id = "mistralai/Mistral-7B-Instruct-v0.3"
device = torch.devices("mps" if torch.backends.mps.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id,torch_dtype = torch.float16).to(device)

def generate_response(prompt):
	inputs = tokenizer(prompt,return_tensors="pt").to(device)
	outputs = model.generate(**inputs,max_tokens=200)
	return tokenizer.decode(outputs[0],skip_special_tokens=True)

def handle_query(uer_input):
	docs = retrieve_docs(user_input)
	context = " ".join(docs)

	specialist = get_specialist_openbio(user_input)
	if specialist:
		doctors = find_doctors(specialist)
		doctor_info = "\n".join([
			f"{d['name']}-{d['designation']}@{d[hospital]},{d['location']}"
			for d in doctors
		])
		return{
			"response":f"It seems like you may need to consult a {specialist}.\n Here are some options:\n{doctor_info}"
		}

	prompt = f"Context: {context}\n\nQuestion: {user_input}\nAnswer:"
	answer = generate_response(prompt)
	return {"response":answer}