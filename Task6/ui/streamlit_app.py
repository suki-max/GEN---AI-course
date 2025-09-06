import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.qa_chain import get_qa_chain

# ✅ Page settings
st.set_page_config(page_title="📚 Scientific QA Bot", layout="centered")
st.title("📚 Smart Scientific Chatbot (arXiv)")

# ✅ Load QA chain
qa_chain = get_qa_chain()

# ✅ User input
query = st.text_input("Ask a research question (Computer Science related):")

# ✅ Handle query
if query:
    with st.spinner("Thinking..."):
        try:
            response = qa_chain.invoke({"question": query})
            st.markdown(f"**Answer:** {response['text']}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
