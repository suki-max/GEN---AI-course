from langchain_huggingface import HuggingFaceEmbeddings

def get_embedder():
    model_name = "all-MiniLM-L6-v2"  # small and fast
    return HuggingFaceEmbeddings(model_name=model_name)
