from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import RetrievalQA

def get_qa_chain(vector_store):
    # Free, small, CPU model
    hf_pipeline = pipeline(
        "text-generation",
        model="distilgpt2",
        tokenizer="distilgpt2",
        max_new_tokens=100,       # ✅ This is the key fix
        temperature=0.7,
        pad_token_id=50256        # prevent warning from GPT2 tokenizer
    )

    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever()
    )
