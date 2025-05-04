from llm_model import generate_answer

query = "I have chest pain what to do?"
prompt = f"""You are a helpfull medical assistant.
User:{query}
Answer:"""

response = generate_answer(prompt)
print("LLM Response:\n",response)