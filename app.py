# streamlit_app.py (Streamlit frontend)
import streamlit as st
import requests

st.set_page_config(page_title="🔍 Multi-LLM Article Bot")
st.title("❓ Multi-LLM Article Generator")

prompt = st.text_area("Your prompt:", height=150)
model = st.radio("Choose LLM:", ("Mixtral", "LLaMA", "Mistral"))

if st.button("Generate Article"):
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating..."):
            try:
                res = requests.post(
                    "http://127.0.0.1:5000/chat",
                    json={"prompt": prompt, "model": model},
                    timeout=90
                )
                res.raise_for_status()
                data = res.json()
            except Exception as e:
                st.error(f"Error: {e}")
            else:
                # Display category and generated article
                st.success(f"Category: **{data['category']}**")
                st.subheader("Article Output:")
                st.write(data["article"])
                # Save to history
                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.insert(0, (model, data["article"]))

# Show history if any
if st.session_state.get("history"):
    st.subheader("🕒 History")
    for i, (m, txt) in enumerate(st.session_state.history):
        st.markdown(f"**{i+1}. {m}** – {txt[:200]}…")