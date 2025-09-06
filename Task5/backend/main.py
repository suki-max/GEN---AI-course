from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from io import BytesIO
from PIL import Image

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/chat")
async def chat(prompt: str):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return {"response": response.text}

@app.post("/vision")
async def vision(prompt: str, file: UploadFile = File(...)):
    img = Image.open(BytesIO(await file.read()))
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([prompt, img])
    return {"response": response.text}

@app.post("/generate_image")
async def generate_image(prompt: str):
    model = genai.GenerativeModel("imagen-3.0")
    response = model.generate_content(prompt)
    return {"image_url": response.candidates[0].content.parts[0].text}
