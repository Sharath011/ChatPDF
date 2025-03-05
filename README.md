# ChatPDF

ChatPDF is a web application that allows users to upload PDF files and chat with an LLM (Large Language Model) about the document's content. The chatbot provides responses with citations from the specific chunks of the PDF. This project uses **FastAPI** for the backend, **React (Vite)** for the frontend, and **Ollama** for local LLM inference.

## Features
- Upload a **single PDF** or a **folder of PDFs**.
- Query the chatbot about the document.
- LLM-generated responses include citations from the document.
- Supports local inference using **Ollama**.
- Deploy the frontend using **Vercel**.

## Tech Stack
### Backend:
- **FastAPI** (Python)
- **pymupdf** (PDF parsing)
- **Ollama** (local LLM inference)
- **LangChain** (embedding & retrieval)
- **Faiss** (Vector Store for efficient retrieval)

### Frontend:
- **React (Vite)**
- **Tailwind CSS**
- **Axios** (API requests)

### Deployment:
- **Vercel** (Frontend)
- **Localhost** (Backend for now)

---

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- **Python 3.10+**
- **Node.js 18+**
- **pip & virtualenv** (for Python dependencies)
- **Vercel CLI** (for deployment)

### 1️⃣ Backend Setup (FastAPI)
#### Clone the repository:
```sh
 git clone https://github.com/your-repo/ChatPDF.git
 cd ChatPDF/backend
```

#### Create a virtual environment and install dependencies:
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Run the backend server:
```sh
uvicorn main:app --reload
```
Server should now be running at: **http://127.0.0.1:8000**

---

### 2️⃣ Frontend Setup (React + Vite)
#### Navigate to frontend and install dependencies:
```sh
cd ../frontend
npm install
```

#### Run the frontend locally:
```sh
npm run dev
```

The frontend should be running at **http://localhost:5173**

---

## Deployment
### Deploying the Frontend with Vercel
#### 1. Install Vercel CLI
```sh
npm install -g vercel
```

#### 2. Login to Vercel
```sh
vercel login
```

#### 3. Deploy the frontend
```sh
vercel
```
Follow the prompts to set up the project and deploy. Once completed, you’ll get a **Vercel-hosted URL**.

---

## Usage
1. Upload a **PDF** or **folder of PDFs** from the frontend.
2. Type a query about the document’s contents.
3. The chatbot responds with relevant information, including citations.

---

## Troubleshooting
- **Frontend Fails to Start?**  
  Ensure `vite.config.js` has the correct imports and run:
  ```sh
  npm install
  ```

- **Backend Module Not Found?**  
  Activate the virtual environment before running FastAPI:
  ```sh
  source venv/bin/activate  # Windows: venv\Scripts\activate
  ```

- **Vercel Deployment Issues?**  
  Make sure `package.json` has the correct build scripts:
  ```json
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
  ```

---

## License
This project is licensed under the MIT License.

---

## Contact
For any questions or issues, reach out via [GitHub Issues](https://github.com/your-repo/ChatPDF/issues).

