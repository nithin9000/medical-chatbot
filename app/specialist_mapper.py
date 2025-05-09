from transformers import AutoTokenizer,AutoModelForCausalLM
import torch

model_id = "mistralai/Mistral-7B-Instruct-v0.3"
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

tokenizer = Autotokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id,torch_dtype=torch.float16).to(device)
specialist_map = {
	"chest pain":"Cardiologist",
	"shortness of breath":"Pulmonologist",
	"skin rash":"Dermatologist",
	"fever":"General physician",
	"joint pain":"Orthopediac",
	"headache":"Neurologist",
	"eye pain":"Ophthamologist",
	"stomach ache":"Gastroenologist"
}

def extract_symptom_with_openbio(user_input):
	prompt = f"""You are a helpfull medical assistant.
	Identify the main symptom in the user's message and return it in one short phrase.
	User message : "{user_input}"
	Symptom:"""

	inputs = tokenizer(prompt,return_tensors="pt",return_token_type_ids=False).to(device)
	outputs = model.generate(**inputs,max_new_tokens=20)
	response = tokenizer.decode(outputs[0],skip_special_tokens=True)
	symptom = response.split("Symptom:")[-1].strip().lower()
	return symptom

def get_specialist_openbio(user_input):
	symptom = extract_symptom_with_openbio(user_input)
	for key in specialist_map:
		if key in symptom:
			return specialist_map[key]
	return "General physician"