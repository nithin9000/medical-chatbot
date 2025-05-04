from transformers import AutoModelForCausalLM,AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("aaditya/Llama3-OpenBioLLM-8B")
model = AutoModelForCausalLM.from_pretrained("aaditya/Llama3-OpenBioLLM-8B")

def generate_answer(prompt:str,max_tokens:int=300) -> str:
	inputs = tokenizer(prompt,return_tensors="pt").to("cuda")
	outputs = model.generate(**inputs,max_new_tokens=max_tokens)
	return tokenizer.decode(outputs[0],skip_special_tokens==True)