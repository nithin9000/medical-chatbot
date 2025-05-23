import requests
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
    PromptTemplate,
    Settings)
from langchain_huggingface import HuggingFaceEmbeddings
from llama_index.llms.ollama import Ollama
from model.utils import EMBEDDING_MODEL_NAME

OLLAMA_URL = "http://localhost:11434/api/generate"
#OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


embed_model = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL_NAME)
Settings.embed_model = embed_model

storage_context = StorageContext.from_defaults(persist_dir="/Users/nithin/Developer/medical-chatbot/backend/vector_index")
index = load_index_from_storage(storage_context)

system_prompt = """<|SYSTEM|># You are an AI-enabled medical chatbot.
Your goal is to answer questions accurately using only the context provided."""

query_wrapper_prompt = PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>")


llm = Ollama(
    model="mistral:7b",
    request_timeout=60.0,
    base_url="http://localhost:11434",
    system_prompt=system_prompt,
    query_wrapper_prompt=query_wrapper_prompt
)

Settings.llm = llm
query_engine = index.as_query_engine(similarity_top_k = 5)

def generate_response(prompt: str) -> str:
#def generate_response(question:str,context:str) -> str:
    try:
        nodes = query_engine.retrieve(prompt)
        context = "\n\n".join([node.get_content() for node in nodes])
        print("\n📚 Retrieved RAG Context:\n",context,"\n")

        SYSTEM_PROMPT = (
            "You are MedBot, a helpful and professional medical assistant. "
            "You can only answer questions related to medicine, healthcare, diseases, symptoms, treatments, doctors, and wellness. "
            "If the user asks anything outside the medical domain, respond with:\n"
            "'I'm sorry, I can only assist with medical-related queries.'\n\n"
            "Use the provided context to answer to answer the question as accurately as possible.\n\n"
            f"Context:\n{context.strip()}"
        )

        full_prompt= (
            f"<|system|>\n{SYSTEM_PROMPT}\n"
            f"<|user|>\n{prompt.strip()}\n"
            f"<|assistant|>\n"
        )

        payload = {
            "model": "mistral:7b",
            #"model":"llava-llama3:8b",
            "prompt": full_prompt,
            "stream": False
        }
        res = requests.post(OLLAMA_URL, json=payload)
        return res.json().get("response","").strip()
    except Exception as e:
        return f"❌ Ollama error: {str(e)}"
