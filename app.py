import streamlit as st
from language_utils import detect_language
from translator import Translator

st.set_page_config("Multilingual Chatbot", layout="wide")
translator = Translator()

if "history" not in st.session_state:
    st.session_state.history = []

# Detect user language
user_input = st.chat_input("Type your message here...")
if user_input:
    src = detect_language(user_input)
    tgt = 'en_XX'  # Assuming chatbot’s original language is English

    # Translate user input to English
    in_eng = translator.translate(user_input, src, tgt)
    st.session_state.history.append(("user", user_input))

    # Generate response (mock / default)
    response_eng = f"I understood: {in_eng}"

    # Translate back to user's language
    response_user = translator.translate(response_eng, 'en_XX', src)
    st.session_state.history.append(("bot", response_user))

# Display chat history
for speaker, message in st.session_state.history:
    with st.chat_message("user" if speaker == "user" else "assistant"):
        st.write(message)
