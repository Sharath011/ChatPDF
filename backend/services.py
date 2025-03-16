# /backend/services.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_ollama import OllamaLLM

# ChromaDB storage path
CHROMA_DB_PATH = "backend/chroma_db"

# Load embeddings
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        texts = [doc.page_content for doc in documents]
        return texts
    except Exception as e:
        print(f"Error extracting text: {e}")
        return []

def get_vectorstore():
    """Initializes or loads the Chroma vectorstore."""
    return Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embedding_function)

def query_pdf(vectorstore, query, model):
    """Runs the query on the stored PDF data using the selected LLM."""
    retriever = vectorstore.as_retriever()
    
    try:
        if model == "openai":
            llm = OpenAI()
        elif model == "mistral":
            llm = OllamaLLM(model="mistral")
        else:
            return "Invalid model selection."

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, retriever=retriever, return_source_documents=True
        )
        
        response = qa_chain.invoke({"query": query})
        return response["result"]  # Extract the answer
    except Exception as e:
        return f"Error in processing query: {e}"