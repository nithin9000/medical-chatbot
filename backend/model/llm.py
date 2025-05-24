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

embed_model = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL_NAME)
Settings.embed_model = embed_model

storage_context = StorageContext.from_defaults(persist_dir="./vector_index")
index = load_index_from_storage(storage_context)

system_prompt = """<|SYSTEM|># You are MedMistral,an AI-enabled professional medical assistant.
You only answer to health related queries.if the question is unrelated to medicine,reply:
"I'm sorry,I can only assist with medical-related queries." """

query_wrapper_prompt = PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>")


llm = Ollama(
    model="mistral:7b-instruct",
    request_timeout=60.0,
    base_url="http://localhost:11434",
    system_prompt=system_prompt,
    query_wrapper_prompt=query_wrapper_prompt
)

Settings.llm = llm
query_engine = index.as_query_engine(similarity_top_k = 5)

def generate_response(prompt: str,chat_history:str = " ") -> str:
#def generate_response(question:str,context:str) -> str:
    try:
        nodes = query_engine.retrieve(prompt)
        context = "\n\n".join([node.get_content() for node in nodes])
        print("\n📚 Retrieved RAG Context:\n",context,"\n")

        SYSTEM_PROMPT = (
            "You are MedMistral, a helpful and professional medical assistant. "
            "You can only answer questions related to medicine, healthcare, diseases, symptoms, treatments, doctors, and wellness. "
            "If the user asks anything outside the medical domain, respond with:\n"
            "'I'm sorry, I can only assist with medical-related queries.'\n\n"
            "Use the provided context to answer the question as accurately as possible.\n\n"
            f"Context:\n{context.strip()}/n/n"
            "Use the provided chat history to Understand context from previous messages and respond accordingly.\n\n"
            f"Chat history:\n{chat_history.strip()}"
            f"User:{prompt.strip()}"
        )

        full_prompt= (
            f"<|system|>\n{SYSTEM_PROMPT}\n"
            f"<|user|>\n{prompt.strip()}\n"
            f"<|assistant|>\n"
        )

        payload = {
            "model": "mistral:7b-instruct",
            #"model":"llava-llama3:8b",
            "prompt": full_prompt,
            "stream": False
        }
        res = requests.post(OLLAMA_URL, json=payload)
        return res.json().get("response","").strip()
    except Exception as e:
        return f"❌ Ollama error: {str(e)}"
