import streamlit as st
import requests

st.set_page_config(page_title="Medical Q&A Chatbot")
st.title("🩺 Medical Q&A Chatbot (MedQuAD)")

q = st.text_input("Ask a medical question:")
if st.button("Submit"):
    if not q.strip():
        st.warning("Please type a question 😊")
    else:
        with st.spinner("Fetching answer..."):
            try:
                r = requests.post("http://localhost:5000/chat", json={"question": q})
                r.raise_for_status()
            except requests.RequestException as e:
                st.error(f"Failed to reach API: {e}")
            else:
                ans = r.json()
                if ans.get("error"):
                    st.error(ans["error"])
                else:
                    st.markdown(f"**Answer:** {ans.get('answer','—')}")
                    if 'question' in ans and 'similarity' in ans:
                        st.markdown(f"**Matched Question:** {ans['question']} "
                                    f"(Similarity: {ans['similarity']:.2f})")
                    if ans.get('entities'):
                        st.markdown("**Recognized Medical Entities:**")
                        for ent, label in ans['entities']:
                            st.write(f"- {ent} ({label})")
