import os
import logging
import sys
from dotenv import load_dotenv
from huggingface_hub import login
from langchain_huggingface import HuggingFaceEmbeddings
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    PromptTemplate,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.llms.ollama import Ollama
from utils import check_memory_usage, EMBEDDING_MODEL_NAME

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


load_dotenv()
hf_key = os.getenv("HF_KEY")
if not hf_key:
    raise ValueError("❌ HF_KEY not found in environment.")
os.environ["HF_KEY"] = hf_key
login(token=hf_key, add_to_git_credential=True)


papers_directory = "./backend/rag_index"
index_dir = './backend/vector_index'

if os.path.exists(index_dir) and os.listdir(index_dir):
    print("Loading existing index from disk....")
    embed_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    Settings.embed_model = embed_model
    storage_context = StorageContext.from_defaults(persist_dir = index_dir)
    index = load_index_from_storage(storage_context)
else:
    print("📄 Building index from PDFs...")
    def find_all_pdfs(directory):
        pdf_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    full_path = os.path.join(root, file)
                    pdf_files.append(full_path)
        print(f"📄 Found {len(pdf_files)} PDFs:")
        for f in pdf_files:
            print("   ➜", f)
        return pdf_files

    pdf_files = find_all_pdfs(papers_directory)
    if not pdf_files:
        print("❌ No PDF files found. Please add them to:", papers_directory)
        sys.exit()

    try:
        reader = SimpleDirectoryReader(
            input_dir=papers_directory,
            recursive=True,
            required_exts=[".pdf"]
        )
        documents = reader.load_data()
        print(f"✅ Loaded {len(documents)} documents")
    except Exception as e:
        logging.error(f"❌ Failed to load documents: {e}")
        documents = []

    if not documents:
        print("❌ No documents loaded.")
        sys.exit()

    embed_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    Settings.embed_model = embed_model

    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

    index.storage_context.persist(persist_dir = index_dir)
    print(f"Index saved to {index_dir}")

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
Settings.chunk_size = 1024

query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)


done = False
while not done:
    print("*" * 30)
    question = input("Enter your question: ")
    response = query_engine.query(question)
    print(response)
    done = input("End the chat? (y/n): ").lower() == "y"



'''import os
import logging
import sys
from dotenv import load_dotenv
from huggingface_hub import login
from langchain_huggingface import HuggingFaceEmbeddings
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
from langchain.prompts import PromptTemplate
from model.utils import check_memory_usage, EMBEDDING_MODEL_NAME

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Load HuggingFace key
load_dotenv()
hf_key = os.getenv("HF_KEY")
if not hf_key:
    raise ValueError("HF_KEY not set in environment")
os.environ["HF_KEY"] = hf_key
login(token=hf_key, add_to_git_credential=True)

# Directory with PDFs
papers_directory = "/Users/nithin/Developer/medical-chatbot/backend/paper"

# Confirm PDF presence
def find_all_pdfs(directory):
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    print(f"📄 Found {len(pdf_files)} PDFs:")
    for f in pdf_files:
        print("   ➜", f)
    return pdf_files

pdf_files = find_all_pdfs(papers_directory)
if not pdf_files:
    print("❌ No PDFs found. Check your path or files.")
    sys.exit()

# Load documents once
try:
    reader = SimpleDirectoryReader(
        input_dir=papers_directory,
        recursive=True,
        required_exts=[".pdf"]
    )
    documents = reader.load_data()
    print(f"✅ Loaded {len(documents)} chunks from PDFs.")
except Exception as e:
    logging.error(f"❌ Failed to load documents: {e}")
    sys.exit()

# Embedding
embed_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
Settings.embed_model = embed_model

# Vector index
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

# Prompt setup
system_prompt = (
    "You are MedBot, a professional medical assistant. "
    "You ONLY answer health-related questions. If the question is unrelated, respond with: "
    "'I'm sorry, I can only assist with medical-related queries.'"
)

# Correct template for prompt wrapping
query_wrapper_prompt = PromptTemplate.from_template(
    "{query_str}"
)

# Ollama LLM
llm = Ollama(
    model="mistral:7b",
    request_timeout=60.0,
    base_url="http://localhost:11434",
    system_prompt=system_prompt,
    query_wrapper_prompt=query_wrapper_prompt
)

Settings.llm = llm
Settings.chunk_size = 1024

query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)

# Interactive loop
done = False
while not done:
    print("*" * 30)
    question = input("Enter your question: ").strip()
    if not question:
        continue
    response = query_engine.query(question)
    print(response)
    done = input("End the chat? (y/n): ").strip().lower() == "y"
'''

'''
import os,logging,sys,psutil,joblib,pickle,json
import torch

from model.utils import check_memory_usage,EMBEDDING_MODEL_NAME

from langchain.prompts import PromptTemplate
from huggingface_hub import login
from langchain_huggingface import HuggingFaceEmbeddings
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,PromptTemplate,Settings
#from llama_index.llms.ollama import Ollama
from llama_index.llms.ollama import Ollama
from IPython.display import HTML,display
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stdout,level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()
hf_key = os.getenv("HF_KEY")
if hf_key is None:
    raise ValueError("HF_Key not set in environment")
os.environ["HF_KEY"] = hf_key
login(token=hf_key,add_to_git_credential=True)

papers_directory = "/Users/nithin/Developer/medical-chatbot/backend/paper"

def find_all_pdfs(directory):
    pdf_files = []
    #print(f"PDFs found {len(pdf_files)} PDFs")
    for root,_,files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root,file))
    return pdf_files

def find_all_pdfs(directory):
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(root, file)
                pdf_files.append(full_path)
    print(f"📄 Found {len(pdf_files)} PDFs:")
    for f in pdf_files:
        print("   ➜", f)
    return pdf_files


pdf_files = find_all_pdfs(papers_directory)

documents = []

#def check_memory_usage(threshold=80):
#	memory = psutil.virtual_memory()
#	return memory.percent < threshold

batch_size = 10

for i in range(0,len(pdf_files),batch_size):
    if not check_memory_usage():
        logging.warning("Memory usage is high,pause the process.")
        break
    batch = pdf_files[i:i+batch_size]
    for pdf_file in batch:
        try:
            reader = SimpleDirectoryReader(input_dir=os.path.dirname(pdf_file),required_exts=".pdf").load_data()
            documents.extend(reader)\
            #reader = SimpleDirectoryReader(input_dir=papers_directory,recursive=True,required_exts=[".pdf"])
            #documents = reader.load_data()

        except Exception as e:
            logging.error(f"Failed to read {pdf_file}:{e}")
            documents = []

if documents:
    print("█"*30)
    print(documents[0])
else:
    print("No documents found.")

embed_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
index = VectorStoreIndex.from_documents(documents,embed_model = embed_model)

system_prompt = "You are an AI-enabled medical chatbot.Your goal is to answer questions accurately using only the context Provided."

query_wrapper_prompt = PromptTemplate.from_template(
    f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{query_str}\nMedBot:"
)

llm = Ollama(
    model="mistral:7b-instruct",  # or llama2, mistral, etc., depending on your model
    request_timeout=60.0,
    base_url="http://localhost:11434",
    system_prompt = system_prompt,
    query_wrapper_prompt = query_wrapper_prompt
)

Settings.embed_model = embed_model
Settings.llm = llm
Settings.chunke_size = 1024

query_engine = index.as_query_engine(llm=llm,similarity_top_k=5)

done=False
while not done:
    print("*"*30)
    question = input("Enter your question : ")
    response = query_engine.query(question)
    print(response)
    done=input("end the chat?(y/n): ") == "y"
'''