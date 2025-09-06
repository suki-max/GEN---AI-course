import streamlit as st
import sqlite3
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from datetime import datetime
import torch.nn.functional as F

# Load model + tokenizer manually to avoid pipeline/meta tensor issue
try:
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model.eval()  # evaluation mode
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# Define response and emoji maps
response_map = {
    "positive": "That's wonderful to hear! 😊 How can I assist you further?",
    "negative": "I'm sorry to hear that. 😥 Want to talk more about it?",
    "neutral": "Got it. 😐 Tell me more if you’d like.",
}

emoji_map = {
    "positive": "😊",
    "negative": "😥",
    "neutral": "😐",
}

# Connect SQLite
conn = sqlite3.connect('chat_history.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user TEXT,
        bot TEXT,
        sentiment TEXT
    )
''')
conn.commit()

# Sidebar history
st.sidebar.title("Recent Chat History")
cursor.execute("SELECT user, bot, sentiment FROM chats ORDER BY id DESC LIMIT 5")
recent_rows = cursor.fetchall()[::-1]
for row in recent_rows:
    user_msg, bot_msg, sentiment = row
    emoji = emoji_map.get(sentiment, "")
    st.sidebar.write(f"{emoji} You: {user_msg}")
    st.sidebar.write(f"🤖 Bot: {bot_msg}")
    st.sidebar.write("---")

# Title
st.title("Sentiment-Aware Chatbot 🤖")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Text input
user_input = st.text_input("You:", "")

def classify_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)
        label_id = torch.argmax(probs, dim=1).item()
        score = probs[0][label_id].item()
        label = model.config.id2label[label_id].lower()
        return label, score

if st.button("Send"):
    if user_input:
        try:
            label, score = classify_sentiment(user_input)
        except Exception as e:
            st.error(f"Error during sentiment analysis: {e}")
            label = "neutral"
            score = 0.0

        bot_response = response_map.get(label, "I'm here to listen. 🤖")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO chats (timestamp, user, bot, sentiment) VALUES (?, ?, ?, ?)",
            (timestamp, user_input, bot_response, label)
        )
        conn.commit()

        st.session_state.messages.append(("user", user_input))
        st.session_state.messages.append(("assistant", bot_response))

        st.write(f"**Detected sentiment:** {label} (score: {score:.2f})")

# Display messages
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.write(message)
