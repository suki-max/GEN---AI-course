import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# Load dataset
df = pd.read_csv('data/medquad.csv')
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.9)
X = vectorizer.fit_transform(df['question'])

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

def extract_entities(text: str):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def get_answer(user_q: str):
    entities = extract_entities(user_q)
    user_vec = vectorizer.transform([user_q])
    sims = cosine_similarity(user_vec, X).flatten()
    idx = sims.argmax()
    return {
        'answer': df.iloc[idx]['answer'],
        'question': df.iloc[idx]['question'],
        'similarity': float(sims[idx]),
        'entities': entities
    }
