import os,logging,sys,psutil,joblib,pickle,json
import torch

from utils import check_memory_usage,EMBEDDING_MODEL_NAME

from huggingface_hub import login
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,PromptTemplate,Settings
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

papers_directory = "rag_index/"

def find_all_pdfs(directory):
	pdf_files = []
	for root,_,files in os.walk(directory):
		for file in files:
			if file.endswith('.pdf'):
				pdf_files.append(os.path.join(root,file))
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
			documents.extend(reader)

		except Exception as e:
			logging.warning(f"Failed to read {pdf_file}:{e}")

if documents:
	print("█"*30)
	print(documents[0])
else:
	print("No documents found.")

embed_model = HuggingFaceBgeEmbeddings(model_name=EMBEDDING_MODEL_NAME)

index = VectorStoreIndex.from_documents(documents,embed_model = embed_model)

system_prompt = """<|SYSTEM|># You are an AI-enabled medical chatbot.
Your goal is to answer questions accurately using only the context Provided."""

query_wrapper_prompt = PromptTemplate("<|USER|>{quey_str}<|ASSISTANT|>")

llm = Ollama(
    model="deepseek:14b",  # or llama2, mistral, etc., depending on your model
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