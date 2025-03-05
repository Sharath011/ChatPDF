import os
import PyPDF2
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from llama_cpp import Llama

VECTOR_STORE_PATH = "embeddings"
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

chroma_client = chromadb.PersistentClient(VECTOR_STORE_PATH)
collection = chroma_client.get_or_create_collection(name="pdf_chunks")

def process_pdf(file_paths):
    all_chunks = []
    for file_path in file_paths:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

        doc_chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        docs = [Document(page_content=chunk, metadata={"source": file_path}) for chunk in doc_chunks]

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2").embed_documents([d.page_content for d in docs])
        for doc, embedding in zip(docs, embeddings):
            collection.add(documents=[doc.page_content], metadatas=[doc.metadata], embeddings=[embedding])

        all_chunks.extend(docs)
    return all_chunks

def chat_with_llm(query, model):
    results = collection.query(query_texts=[query], n_results=3)
    context_chunks = [result["document"] for result in results["documents"]]
    citations = [result["metadata"]["source"] for result in results["documents"]]

    context = "\n".join(context_chunks)
    final_prompt = f"Context:\n{context}\n\nUser: {query}\nAI:"

    if model == "openai":
        llm = ChatOpenAI()
        response = llm.predict(final_prompt)
    else:
        llm = Llama(model_path=f"models/{model}.gguf", n_gpu_layers=30)
        response = llm(final_prompt)

    return response, citations
