from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,ServiceContext
from llama_index.vector_stores.faiss import FaissVectorStore
from sentence_transformers import SentenceTransformers
from llama_index.embeddings.langchain import LangchainEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import faiss
import os
import numpy as np

embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
embed_model = LangchainEmbeddings(embedding_model)

service_context = ServiceContext.from_defaults(embed_model=embed_model)

def build_index(doc_dir = "data/medical_docs",index_dir="vector_store/faiss_index"):
	documents = SimpleDirectoryReader(doc_dir).load_data()

	texts = [doc.text for doc in documents]
	vectors = embedding_model.embed_documents(texts)

	dim = len(vectors[0])
	faiss_index = faiss.IndexFlatL2(dim)
	faiss_index.add(np.array(vectors))

	faiss.write_index(faiss_index,os.path.join(index_dir,"index.faiss"))
	with open(os.path.join(index_dir,"docs.txt"),"w") as f:
		f.write("/n".join(texts))

	vector_store = FaissVectorStore(faiss_index=faiss_index)
	index = VectorStoreIndex.from_documents(documents,vector_store=vector_store,service_context=service_context)
	return index

def retrive_docs(query,index_dir = "vectorstore/faiss_index",top_k=3):
	faiss_index = faiss.read_index(os.path.join(index_dir,"index.faiss"))
	with open(os.path.join(index_dir,"docs.txt"),"r") as f:
		docs = f.readlines()

	query_vec = embedding_model.embed_query(query)
	_,I = faiss_index.search(np.array([query_vec]),top_k)
	return [docs[i].strip() for i in I[0]]