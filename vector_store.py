import os
import pickle
from langchain_community.vectorstores import FAISS
from .data_ingestion import load_documents
from .embedder import get_embedder
from langchain.schema import Document

def save_vector_store(vstore, path="vectorstore/faiss_store.pkl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(vstore, f)

def create_vector_store(docs, embedder):
    texts = [doc["text"] for doc in docs]
    metadata = [{"source": doc["filename"]} for doc in docs]
    documents = [Document(page_content=texts[i], metadata=metadata[i]) for i in range(len(texts))]
    return FAISS.from_documents(documents, embedder)

def load_vector_store(embedder, path="vectorstore/faiss_store.pkl"):
    if not os.path.exists(path):
        docs = load_documents()
        vs = create_vector_store(docs, embedder)
        save_vector_store(vs, path)
        return vs
    with open(path, "rb") as f:
        return pickle.load(f)
