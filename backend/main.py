# /backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from services import extract_text_from_pdf, get_vectorstore, query_pdf

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploads folder
UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize vectorstore
vectorstore = get_vectorstore()

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    try:
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text and store in vectorstore
        texts = extract_text_from_pdf(file_path)
        if not texts:
            raise HTTPException(status_code=400, detail="No text extracted from PDF")

        vectorstore.add_texts(texts)
        vectorstore.persist()
        return JSONResponse(content={"message": "PDF uploaded and processed successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define request body model
class ChatRequest(BaseModel):
    query: str
    model: str

@app.post("/chat/")
async def chat_with_pdf(request: ChatRequest):
    try:
        response = query_pdf(vectorstore, request.query, request.model)
        return JSONResponse(content={"response": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/")
async def get_available_models():
    """Returns the list of available LLMs"""
    return JSONResponse(content={"models": ["openai", "mistral"]})