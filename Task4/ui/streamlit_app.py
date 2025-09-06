import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.vector_store import load_vector_store
from app.embedder import get_embedder
from app.retriever import get_qa_chain
from app.scheduler import start_scheduler
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Smart QA Chatbot", layout="wide")

embedder = get_embedder()
vector_store = load_vector_store(embedder)
qa_chain = get_qa_chain(vector_store)

st.title("📚 Smart QA Chatbot")

query = st.text_input("Ask a question about your knowledge base")

if query:
    response = qa_chain.run(query)
    st.markdown(f"**Answer:** {response}")

# Start background updater
start_scheduler()
