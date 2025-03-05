from fastapi import FastAPI, UploadFile, File, Form
import os
import shutil
import fitz  # PyMuPDF
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Directories
UPLOAD_FOLDER = "uploaded_pdfs"
VECTORSTORE_DIR = "chroma_db"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize FastAPI
app = FastAPI()

# Load Embedding Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = "\n\n".join([page.get_text("text") for page in doc])
    return text


def store_pdf_embeddings(pdf_path):
    """Extracts text from a PDF, splits it, and stores embeddings in ChromaDB."""
    text = extract_text_from_pdf(pdf_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.create_documents([text])
    
    vectorstore = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)
    vectorstore.add_documents(texts)


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """API endpoint to upload a PDF, process it, and store embeddings."""
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    store_pdf_embeddings(file_path)
    
    return {"filename": file.filename, "message": "PDF uploaded and processed"}


@app.post("/chat/")
async def chat_with_pdf(query: str = Form(...)):
    """API endpoint to search the vector database for relevant content."""
    vectorstore = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)
    docs = vectorstore.similarity_search(query, k=3)
    response = "\n\n".join([doc.page_content for doc in docs])
    
    return {"response": response}
