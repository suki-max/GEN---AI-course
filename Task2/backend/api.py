# api.py (Flask backend)
import os
import joblib
from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)
BASE = os.path.dirname(__file__)

# Load your classifier
clf = joblib.load(os.path.join(BASE, 'model', 'tfidf_model.pkl'))

# Hugging Face token
HF_TOKEN = "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"

# Generation pipeline loader (no quantization for CPU)
def load_gen(model_id):
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        token=HF_TOKEN
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        token=HF_TOKEN,
        device_map="auto"
    )
    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )

# Load all LLMs
llm_mixtral = load_gen("mistralai/Mixtral-8x7B-Instruct-v0.1")
llm_llama   = load_gen("meta-llama/Meta-Llama-3-8B-Instruct")
llm_mistral = load_gen("mistralai/Mistral-7B-Instruct-v0.3")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Prompt empty"}), 400

    model_name = data.get("model", "").lower()
    if model_name == "mixtral":
        generated = llm_mixtral(prompt, max_new_tokens=150)[0]['generated_text']
    elif model_name == "llama":
        generated = llm_llama(prompt, max_new_tokens=150)[0]['generated_text']
    elif model_name == "mistral":
        generated = llm_mistral(prompt, max_new_tokens=150)[0]['generated_text']
    else:
        return jsonify({"error": f"Model '{model_name}' not recognized"}), 400

    category = clf.predict([prompt])[0]
    return jsonify({"model": model_name, "category": category, "article": generated})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
