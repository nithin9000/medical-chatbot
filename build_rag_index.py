import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from llama_index.core import Document,VectorStoreIndex,ServiceContext
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.langchain import LangchainEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.readers.file.base import SimpleDirectoryReader

doc_dir - "data/medical_docs "
index_dir = "vectore_store/faiss_index"
os.makedirs(index_dir,exist_ok=True)

embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
embed_model = LangchainEmbeddings(embedding_model)

service_context = ServiceContext.from_defaults(embed_model=embed_model)

print("Loading Docs")

raw_docs = SimpleDirectoryReader(doc_dir).load_data()

docs = []
for d in raw_docs:
	file_name = d.metadata.get("file_name","")
	topic = file_name.replace(".txt","").replace("_"," ")
	docs.append(Document(
		text = d.text,
		metadata = {"source":"Gale Encyclopedia","topic":topic}
	))

print("Embdeding and indexing documents")
texts = [doc.text for doc in docs]
vectors = embedding_model.embed_documents(texts)

dim = len(vectors[0])
faiss_index = faiss.IndexFlatL2(dim)
faiss_index.add(np.array(vectors))

faiss.write_index(faiss_index,os.path.join(index_dir,"index.faiss"))
with open(os.path.join(index_dir,"docs.txt"),"w",encoding="utf-8") as f:
	f.write("\n\n".join(texts))

print("RAG Index Built and saved")
