from apscheduler.schedulers.background import BackgroundScheduler
from .data_ingestion import load_documents
from .embedder import get_embedder
from .vector_store import create_vector_store, save_vector_store

def update_vector_store_job():
    print("Updating vector store...")
    docs = load_documents()
    embedder = get_embedder()
    vs = create_vector_store(docs, embedder)
    save_vector_store(vs)
    print("Vector store updated.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_vector_store_job, 'interval', hours=24)
    scheduler.start()
