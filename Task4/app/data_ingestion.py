import os
from PyPDF2 import PdfReader

def load_documents(directory="data/documents"):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            path = os.path.join(directory, filename)
            try:
                reader = PdfReader(path)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                if text.strip():
                    documents.append({
                        "text": text,
                        "filename": filename
                    })
                else:
                    print(f"[WARNING] {filename} has no extractable text.")
            except Exception as e:
                print(f"[ERROR] Failed to read {filename}: {e}")
    return documents
