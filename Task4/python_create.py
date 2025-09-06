# create_sample_pdf.py
from fpdf import FPDF
import os

# Ensure the directory exists
os.makedirs("data/documents", exist_ok=True)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, """Welcome to your Smart QA Chatbot!

This is a sample document used for testing vector embedding.

Topics:
- AI
- Machine Learning
- LangChain
- OpenAI APIs
""")

pdf.output("data/documents/sample.pdf")
print("✅ Sample PDF created at data/documents/sample.pdf")
