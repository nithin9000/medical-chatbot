from fastapi import FastAPI,Request
from app.chatbot import handle_query

app = FastAPI()

@app.get("/")
def health_check():
	return{"status":"running"}

@app.post("/chat")
async def chat_endpoint(req:Request):
	data = await req.json()
	user_input = data.get("query")
	return handle_query(user_input)