import os
import sys
import time
import logging
import faiss
import numpy as np

from langchain.embeddings import HuggingFaceEmbeddings
from llama_index.core import SimpleDirectoryReader,VectorStoreIndex

#from llm import generate_response_from_context;
from llm import generate_response
from utils import log_time,check_memory_usage,EMBEDDING_MODEL_NAME

def find_all_pdfs(directory):
	pdf_files = []
	for root,_,files in os.walk(directory):
		for file in files:
			if file.endswith('.pdf'):
				pdf_files.append(os.path.join(root,file))
	return pdf_files

def read_documents():
	papers_directory = "rag_index/"
	logging.basicConfig(stream=sys.stdout,level=logging.INFO)
	logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

	pdf_files = find_all_pdfs(papers_directory)
	documents = []
	batch_size = 10

	for i in range(0,len(pdf_files),batch_size):
		batch = pdf_files[i:i+batch_size]
		for pdf_file in batch:
			try:
				reader = SimpleDirectoryReader(input_dir = os.path.dirname(pdf_file),required_exts=".pdf").load_data()
				documents.extend(reader)
			except Exception as e:
				logging.warning(f"Failed to read{pdf_file}:{e}")

documents = read_documents()

def save_embedding_model(documents):
	embeddings_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

	texts = [doc.text for doc in documents]
	embeddings = [embeddings_model.embed_query(text) for text in texts]
	embeddings_array = np.array(embeddings)

	dimension = embeddings_array.shape[1]
	index = faiss.IndexFlatL2(dimension)
	index.add(embeddings_array)

	os.makedirs("models" , exist_ok = True)
	faiss.write_index(index,'models/index.faiss')
	np.save('models/responses.npy',texts)

	return embeddings_model

def load_embedding_model():
	index = faiss.read_index('models/index.faiss')
	responses = np.load('models/responses.npy',allow_pickle=True)
	embeddings_model = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL_NAME)
	return index,responses,embeddings_model

def find_best_response(text,embeddings_model,index,responses):
	embedding = np.array(embeddings_model.embed_query(text)).reshape(1,-1)
	D,I = index.search(embedding,1)
	return responses(I[0][0])

def build_index():


if __name__ == "__main__":
	index,responses,embeddings_model = load_embedding_model()

	while True:
		input_text = input("\nAsk your medical question(or type 'exit):")
		if input_text.lower() == 'exit':
			break

		best_context = find_best_response(input_text,embeddings_model,index,responses)
		print("\n📄 Best matching Context:\n",best_context)

		response = generate_response(input_text,best_context)
		print("\n🤖 Answer:\n",response)