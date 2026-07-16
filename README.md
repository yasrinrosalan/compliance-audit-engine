# Enterprise Document Compliance & Semantic Audit Engine

A local, zero-cost AI backend for processing and auditing enterprise PDF documents. This project uses a Retrieval-Augmented Generation (RAG) pipeline to perform semantic searches and generate compliance answers without sending sensitive data to the cloud.

## Tech Stack
* **Backend:** FastAPI, Python, SQLAlchemy
* **Asynchronous Queue:** Redis, Celery
* **Database:** PostgreSQL with `pgvector`
* **AI Models:** Ollama (Llama 3 & nomic-embed-text)
* **Infrastructure:** Docker, Docker Compose

## How to Run

1. **Clone the repository:**
```bash
   git clone [https://github.com/yourusername/compliance-audit-engine.git](https://github.com/yourusername/compliance-audit-engine.git)
   cd compliance-audit-engine
```

2. **Start the Docker containers:**
```bash
   docker compose up -d --build
```


3. **Download the AI models (first time only):**
```bash
docker exec -it compliance_ollama ollama pull nomic-embed-text
docker exec -it compliance_ollama ollama pull llama3

```


4. **Open the API Documentation:**
Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to test the endpoints.

## Core API Endpoints

* `POST /api/v1/documents/upload` - Uploads a PDF and sends it to the background worker for extraction and chunking.
* `POST /api/v1/documents/search` - Searches the PostgreSQL vector database for semantically similar text chunks.
* `POST /api/v1/documents/ask` - Uses Llama 3 to generate a final, source-cited answer based on the document context.