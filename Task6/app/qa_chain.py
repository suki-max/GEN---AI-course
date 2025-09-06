from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import torch

def get_qa_chain():
    # ✅ Use a lightweight open model
    model_id = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    # ✅ Use CPU if no GPU
    device = 0 if torch.cuda.is_available() else -1
    print("Device set to use", "cuda" if device == 0 else "cpu")

    # ✅ Setup pipeline
    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512, device=device)

    # ✅ Wrap in LangChain's LLM
    llm = HuggingFacePipeline(pipeline=pipe)

    # ✅ Create prompt template
    prompt = PromptTemplate(
        input_variables=["question"],
        template="Answer the following computer science research question in detail:\n\nQuestion: {question}\n\nAnswer:"
    )

    # ✅ Wrap into an LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)

    return chain
