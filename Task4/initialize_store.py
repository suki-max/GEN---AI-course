from app.data_ingestion import load_documents
from app.embedder import get_embedder
from app.vector_store import create_vector_store, save_vector_store

print("[INFO] Loading documents...")
docs = load_documents()
print(f"[DEBUG] Loaded {len(docs)} documents.")

print("[INFO] Creating embedder...")
embedder = get_embedder()

print("[INFO] Creating vector store...")
vs = create_vector_store(docs, embedder)

print("[INFO] Saving vector store...")
save_vector_store(vs)

print("[SUCCESS] Vector store initialized.")
