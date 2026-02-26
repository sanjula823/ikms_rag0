# IKMS RAG - Evidence-Aware RAG System

A production-ready Multi-Agent RAG system with evidence-aware inline citations, PDF indexing, vector search, and an interactive frontend.

## Features

✨ **Evidence-Aware Answers**
- Inline citations [C1], [C2] in generated answers
- Machine-readable citation mapping with snippet previews
- Verification agent maintains citation consistency

🔍 **PDF Management**
- Upload and index PDFs directly via web UI
- Extract text with automatic chunking
- Support for large documents with metadata tracking
- Namespace-based organization

📚 **Vector Search**
- Fast similarity search using Pinecone vector store
- OpenAI embeddings for semantic understanding
- Configurable result count and filtering

💬 **Q&A with Citations**
- LangGraph linear orchestration (retrieve → answer → verify)
- LLM-powered question answering backed by evidence
- Automatic citation validity checking

🎨 **Modern UI**
- Responsive web interface for PDF upload
- Interactive search with result highlighting
- Real-time API status monitoring
- Citation visualization and source inspection

📊 **Production Ready**
- Comprehensive error handling and logging
- FastAPI with OpenAPI documentation
- Docker containerization
- Unit and integration tests

## Architecture

```
┌─────────────┐
│   User      │
│   (Browser) │
└──────┬──────┘
       │
       ▼
┌────────────────────────┐
│   FastAPI Backend      │
├────────────────────────┤
│ /upload-pdf            │
│ /search                │
│ /qa                    │
│ /index-pdf             │
│ /static (Web UI)       │
└────────┬───────┬───────┘
         │       │
         ▼       ▼
    ┌─────────┐  ┌──────────────┐
    │ Pinecone│  │ LangGraph    │
    │ Vector  │  │ Agent Flow   │
    │ Store   │  │ (LangChain)  │
    └─────────┘  └──────────────┘
         ▲              │
         └──────┬───────┘
                ▼
          ┌──────────────┐
          │ OpenAI       │
          │ LLM & API    │
          └──────────────┘
```

## Setup

### Prerequisites
- Python 3.11+
- OpenAI API key
- Pinecone account and API key
- Docker (optional, for containerization)

### 1. Environment Configuration

Create `.env` file in project root:

```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=pc-...
PINECONE_INDEX=ikms-rag
PINECONE_ENV=gcp-starter
LOG_LEVEL=INFO
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the API

**Development mode:**
```bash
cd backend/src
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
cd backend/src
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- 🌐 **Web UI**: http://localhost:8000/static/index.html
- 📚 **API Docs**: http://localhost:8000/docs
- ✅ **Health**: http://localhost:8000/health

## API Endpoints

### POST /upload-pdf
Upload and index a PDF file.

**Request:**
```bash
curl -X POST "http://localhost:8000/upload-pdf" \
  -F "file=@document.pdf" \
  -F "namespace=documents"
```

**Response:**
```json
{
  "chunks_indexed": 45,
  "source": "document.pdf",
  "pages": 10
}
```

### POST /search
Search indexed PDFs using vector similarity.

**Request:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "top_k": 5
  }'
```

**Response:**
```json
{
  "query": "What is machine learning?",
  "count": 3,
  "results": [
    {
      "content": "Machine learning is a subset of artificial intelligence...",
      "page": 5,
      "source": "document.pdf",
      "score": 0.92
    }
  ]
}
```

### POST /qa
Ask a question with evidence-aware answers and citations.

**Request:**
```bash
curl -X POST "http://localhost:8000/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain neural networks",
    "top_k": 4
  }'
```

**Response:**
```json
{
  "answer": "Neural networks are computational models inspired by biological neurons [C1]. They consist of layers of interconnected nodes [C2].",
  "context": "[C1] Chunk from page 3: ...",
  "citations": {
    "C1": {
      "page": 3,
      "snippet": "Neural networks are computational...",
      "source": "document.pdf"
    },
    "C2": {
      "page": 4,
      "snippet": "They consist of layers...",
      "source": "document.pdf"
    }
  }
}
```

### POST /index-pdf
Index a PDF from a file path (for batch operations).

**Request:**
```bash
curl -X POST "http://localhost:8000/index-pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/home/user/documents/research.pdf",
    "namespace": "research"
  }'
```

### GET /health
Check API health and available endpoints.

```bash
curl http://localhost:8000/health
```

## Usage

### Web UI

1. Open http://localhost:8000/static/index.html
2. Upload a PDF using the "Upload PDF" panel
3. Use "Search PDFs" to find documents by topic
4. Click "Ask Q&A" to ask questions with evidence citations

### Python Client Example

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # Upload PDF
        with open("document.pdf", "rb") as f:
            response = await client.post(
                "http://localhost:8000/upload-pdf",
                files={"file": f}
            )
            print(response.json())
        
        # Search
        response = await client.post(
            "http://localhost:8000/search",
            json={"query": "machine learning", "top_k": 5}
        )
        print(response.json())
        
        # QA
        response = await client.post(
            "http://localhost:8000/qa",
            json={"question": "What is deep learning?", "top_k": 4}
        )
        print(response.json())

asyncio.run(main())
```

## Testing

### Run Test Suite

```bash
cd backend
pytest
```

### Quick API Tests

```bash
# Simple synchronous test
python test_api_simple.py

# Comprehensive async tests
python test_api.py
```

### Manual Testing with cURL

```bash
# Check health
curl http://localhost:8000/health

# View OpenAPI docs
curl http://localhost:8000/docs

# Search example
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "your query", "top_k": 5}'
```

## Docker Deployment

### Build Image

```bash
docker build -t ikms-rag:latest .
```

### Run Container

```bash
docker run -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/documents:/app/documents \
  ikms-rag:latest
```

### Docker Compose

```yaml
version: '3.8'

services:
  ikms-rag:
    build: .
    ports:
      - "8000:8000"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      PINECONE_API_KEY: ${PINECONE_API_KEY}
      PINECONE_INDEX: ${PINECONE_INDEX}
      PINECONE_ENV: ${PINECONE_ENV}
    volumes:
      - ./documents:/app/documents
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run with:
```bash
docker-compose up -d
```

## Project Structure

```
IKMS_RAG/
├── backend/
│   ├── src/app/
│   │   ├── main.py              # FastAPI app
│   │   ├── api.py               # Endpoint definitions
│   │   ├── core/
│   │   │   ├── agents/          # LangGraph agents
│   │   │   ├── retrieval/       # Chunk serialization & retrieval
│   │   │   └── vectorstore/     # Pinecone integration
│   │   ├── services/
│   │   │   ├── qa_service.py    # Q&A logic
│   │   │   ├── index_service.py # PDF indexing
│   │   │   └── search_service.py# Vector search
│   │   └── utils/
│   │       ├── logging.py       # Structured logging
│   │       └── text.py          # Text utilities
│   ├── static/
│   │   └── index.html           # Web UI
│   ├── requirements.txt         # Dependencies
│   ├── pytest.ini               # Test config
│   ├── test_api.py              # Async tests
│   └── test_api_simple.py       # Simple tests
├── Dockerfile                   # Container image
├── .env.example                 # Environment template
└── README.md                    # This file
```

## Configuration

### Chunk Settings

Adjust chunking in `backend/src/app/services/index_service.py`:

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,      # Characters per chunk
    chunk_overlap=100    # Overlap between chunks
)
```

### LLM Settings

Modify in `backend/src/app/core/agents/agents.py`:

```python
llm = ChatOpenAI(
    model="gpt-4o-mini",      # Model choice
    temperature=0.7,          # Creativity level
    max_tokens=1024           # Max response length
)
```

### Search Results

Control in `backend/src/app/api.py`:

```python
top_k: int = Field(5, ge=1, le=50)  # Default 5, max 50
```

## Logging

Logs are timestamped and include:
- PDF indexing progress
- Chunk generation
- Retrieved document count
- Citations used in answers
- Verification corrections

Set log level in `.env`:
```env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

## Troubleshooting

### "Pinecone connection failed"
- Check API key in `.env`
- Verify index name matches Pinecone dashboard
- Ensure index has embeddings dimension matching OpenAI (1536)

### "No results returned"
- Upload PDFs first via `/upload-pdf`
- Check namespace matches search namespace
- Verify PDFs have extractable text (not scanned images)

### "Invalid citations in response"
- This is handled automatically by verification agent
- Logs show citation corrections
- Enable DEBUG logging to see details

### API Timeout
- Increase timeout in client
- Check Pinecone query performance
- Reduce `top_k` parameter

## Performance Tuning

### For Large Document Sets
- Use namespaces to organize PDFs
- Increase uvicorn `workers` in production
- Enable caching in Pinecone
- Monitor OpenAI API costs

### For Faster Responses
- Reduce `top_k` default (trades accuracy for speed)
- Use smaller chunk size
- Enable query batching

## Security

For production deployment:
1. Use environment variables for all secrets
2. Enable authentication (add API key validation)
3. Use HTTPS/TLS
4. Implement rate limiting
5. Add request validation
6. Restrict CORS origins

Example:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Authorization"],
)
```

## API Response Time

Typical response times:
- Search: 200-500ms (depends on Pinecone)
- Q&A: 1-3 seconds (includes LLM inference)
- Upload: 1-5 seconds (depends on PDF size)

## Monitoring

Monitor API with:
```bash
# View recent logs
docker logs -f ikms-rag

# Check CPU/Memory
docker stats ikms-rag

# Health checks (continuous)
while true; do curl -s http://localhost:8000/health | jq .; sleep 10; done
```

## Support & Issues

For bugs or questions:
1. Check logs: `LOG_LEVEL=DEBUG`
2. Test with simple queries first
3. Verify `.env` configuration
4. Check API docs at `/docs`

## License

MIT - See LICENSE file

## Contributing

Contributions welcome! Areas:
- Additional LLM models
- Advanced filtering
- Caching strategies
- UI enhancements
- Performance optimization
