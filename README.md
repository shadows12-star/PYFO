<div align="center">

# 📄 AI Document Intelligence

**A lightweight Retrieval-Augmented Generation (RAG) application for grounded, source-cited document Q&A.**

Upload a PDF or TXT file → ask a question in plain English → get an answer backed by the exact chunks it came from.

Developed for the **NidusLab AI Software Engineer Intern Technical Pre-Assessment**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C?style=flat)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-6E56CF?style=flat)](https://www.trychroma.com/)
[![Mistral AI](https://img.shields.io/badge/Mistral%20AI-LLM%20%2B%20Embeddings-FA520F?style=flat)](https://mistral.ai/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](#)

</div>

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [📁 Project Structure](#-project-structure)
- [🧰 Tech Stack](#-tech-stack)
- [⚙️ Installation](#️-installation)
- [🔑 Environment Variables](#-environment-variables)
- [▶️ Run the Application](#️-run-the-application)
- [🔍 How It Works](#-how-it-works)
- [🖼️ Screenshots](#️-screenshots)
- [🧭 Example Workflow](#-example-workflow)
- [🧠 Design Decisions](#-design-decisions)
- [🛡️ Hallucination Control](#️-hallucination-control)
- [✅ Assessment Requirements Covered](#-assessment-requirements-covered)
- [🚀 Possible Future Improvements](#-possible-future-improvements)
- [👤 Author](#-author)

---

## ✨ Features

| | Feature |
|---|---|
| 📤 | Upload **PDF** and **TXT** documents |
| 🧹 | Extract and clean document text |
| ✂️ | Split text into overlapping chunks |
| 🏷️ | Preserve metadata — **page number** and **chunk ID** |
| 🧬 | Generate embeddings using **Mistral AI Embeddings** |
| 🗄️ | Store document vectors in **ChromaDB** |
| 🎯 | Retrieve relevant chunks using **MMR semantic search** |
| 💬 | Generate answers using a **Mistral LLM** |
| 🔒 | Restrict answers strictly to retrieved document context |
| 📎 | Display supporting source chunks with page and chunk info |
| 🖥️ | Simple, interactive UI built with **Streamlit** |

---

## 🏗️ Architecture

```text
📤 User uploads PDF/TXT
        ↓
📥 Document Loader
        ↓
🧹 Text Cleaning
        ↓
✂️ Recursive Character Text Splitter
        ↓
🧬 Mistral Embeddings
        ↓
🗄️ Chroma Vector Store
        ↓
🎯 MMR Retriever
        ↓
📌 Top Relevant Chunks
        ↓
🤖 Mistral LLM
        ↓
✅ Answer + Sources
```

---

## 📁 Project Structure

```text
.
├── app.py                  # Streamlit UI
├── document_processor.py   # Loading, cleaning, chunking, embedding
├── main.py                 # RAG pipeline (retrieval + generation)
├── requirements.txt        # Python dependencies
├── .env.example             # Sample environment file
├── .gitignore               # Excludes .env and other local files

```

### 🗂️ File Responsibilities

| File | Responsibility |
|---|---|
| **`app.py`** | Streamlit user interface — handles document upload, processing, questions, answer display, and source display |
| **`document_processor.py`** | PDF/TXT loading, text cleaning, chunking, metadata assignment, embedding generation, and Chroma vector-store creation |
| **`main.py`** | The RAG pipeline — retrieves relevant chunks, builds the document-grounded prompt, calls the Mistral LLM, returns the answer with source metadata |

---

## 🧰 Tech Stack

- 🐍 **Python**
- 🖥️ **Streamlit**
- 🔗 **LangChain**
- 🤖 **Mistral AI**
- 🗄️ **ChromaDB**
- 📄 **PyPDFLoader**
- ✂️ **RecursiveCharacterTextSplitter**
- 🐳 **Docker And DockerCompose**

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

### 2️⃣ Create a virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

A template is also provided in `.env.example`:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

> ⚠️ **Never commit your real API key to GitHub.** `.env` is already excluded via `.gitignore`.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Streamlit will print a local URL, typically:

```text
http://localhost:8501
```

Open it in your browser. 🌐

---
## 🐳 Run with Docker

Prefer containers over a local virtual environment? The project ships with a `Dockerfile` and `docker-compose.yml` for a one-command setup — no local Python install required.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed
- A `.env` file in the project root (see [Environment Variables](#-environment-variables))

### 1️⃣ Build and start the container

```bash
docker compose up --build
```

### 2️⃣ Open the app

```text
http://localhost:8501
```

### 3️⃣ Stop the container

```bash
docker compose down
```

### ⚙️ What's inside

| File | Purpose |
|---|---|
| **`Dockerfile`** | Builds a `python:3.11-slim` image, installs dependencies from `requirements.txt`, and launches the app with `streamlit run app.py` on `0.0.0.0:8501` |
| **`docker-compose.yml`** | Runs the image, maps port `8501`, injects `MISTRAL_API_KEY` from `.env`, and mounts a named volume for the vector store |
| **`.dockerignore`** | Excludes `.env`, `venv/`, `__pycache__/`, and other local-only files from the build context |

### 🗄️ Persisting the vector store

By default, Chroma runs **in-memory** and the index is rebuilt every time the container restarts. If you'd like uploaded documents to stay indexed across restarts, add a `persist_directory` to the `Chroma.from_documents(...)` call in `document_processor.py`, e.g.:

```python
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="/app/chroma_db"
)
```

The `chroma_data` volume in `docker-compose.yml` is already mapped to `/app/chroma_db`, so once persistence is enabled, indexed documents will survive `docker compose down` / `up`.

### 🔁 Rebuilding after code changes

```bash
docker compose up --build
```

Or, if you only changed dependencies:

```bash
docker compose build --no-cache
```
## 🔍 How It Works

### 1. 📤 Document Upload
The user uploads a PDF or TXT document through the Streamlit interface.

### 2. 🧹 Document Processing
The application:
- extracts the text
- normalizes whitespace
- splits the document into overlapping chunks
- stores metadata such as source name, page number, and chunk ID

### 3. 🧬 Embedding and Vector Storage
Each chunk is converted into a vector using the Mistral embedding model and stored in ChromaDB.

### 4. 🎯 Semantic Retrieval
When the user asks a question, the system performs MMR-based retrieval and selects the most relevant document chunks.

### 5. 🤖 Answer Generation
The retrieved chunks are passed to the Mistral LLM as context. The system prompt instructs the model to:
- use only the supplied document context
- avoid relying on outside knowledge
- return a fallback message when the answer cannot be found in the document

### 6. 📎 Source Attribution
The final response contains:
- the generated answer
- source page number
- chunk ID
- retrieved source text

This helps users verify where the answer came from.

---

## 🖼️ Screenshots


### 🏠 Application Home / Upload Screen
<img width="1280" height="969" alt="image" src="https://github.com/user-attachments/assets/036faa9e-4a3d-4d2c-a8c0-61d203f4e01e" />


### ✅ Document Successfully Processed
<img width="264" height="572" alt="image" src="https://github.com/user-attachments/assets/549d4040-af2c-42d4-9112-b26d042615b1" />


### 💬 Question, Answer, and Sources
<img width="1278" height="1267" alt="image" src="https://github.com/user-attachments/assets/330d7860-c760-465a-95ac-2085e87ab934" />






## 🧭 Example Workflow

```text
1. 📤 Upload a PDF or TXT file
2. 🖱️ Click "Process Document"
3. ⏳ Wait for the document to be chunked and indexed
4. ❓ Enter a question about the uploaded document
5. 🖱️ Click "Ask"
6. 📖 Read the generated answer
7. 📎 Expand the Sources section to inspect supporting chunks
```

---

## 🧠 Design Decisions

**Why Streamlit?**
Streamlit provides a fast way to build an interactive AI prototype while keeping the focus on the document-processing and RAG pipeline.

**Why ChromaDB?**
ChromaDB integrates naturally with LangChain and provides efficient vector-based semantic retrieval for small and medium-scale document applications.

**Why MMR Retrieval?**
Maximal Marginal Relevance balances relevance and diversity, so the retriever is less likely to return several nearly identical chunks.

**Why Chunk Overlap?**
Overlap helps preserve context when important information falls near a chunk boundary.

**Why Source Attribution?**
Displaying the retrieved source chunks makes the system transparent and lets users verify whether an answer is actually supported by the document.

---

## 🛡️ Hallucination Control

The application instructs the LLM to answer **only** from the retrieved document context.

If the required information is unavailable, the fallback response is:

```text
I could not find the answer in the document.
```

This reduces the chance of confidently generating unsupported information.

---

## ✅ Assessment Requirements Covered

| Requirement | Status |
|---|:---:|
| PDF/TXT upload | ✅ |
| Text extraction | ✅ |
| Text cleaning | ✅ |
| Chunking | ✅ |
| Page/chunk metadata | ✅ |
| Embeddings | ✅ |
| Vector database | ✅ |
| Semantic retrieval | ✅ |
| RAG pipeline | ✅ |
| LLM-based answers | ✅ |
| Source attribution | ✅ |

---

## 🚀 Possible Future Improvements

- 🔁 Conversation memory for follow-up questions
- 🔎 Hybrid semantic + keyword search
- 📊 Retrieval and answer evaluation
- ⚡ Streaming LLM responses
- 🎚️ Similarity-score thresholding
- 🗃️ Multiple-document management
- 🧯 Better error handling and validation

---

## 👤 Author

**Asiful Alam Sami**  
AI Software Engineer Intern Candidate

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/shadows12-star)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sami-alamm/)
