# R2R Ultra API - REST Endpoints

REST API wrapper for R2R Ultra MCP Server. Provides HTTP endpoints for all MCP tools, resources, and prompts.

## Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn httpx python-dotenv

# Configure environment
cp .env.example .env
# Edit .env with your R2R_BASE_URL and API_KEY

# Run API server
python api.py
```

API will be available at: **http://localhost:8001**

## Documentation

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI JSON**: http://localhost:8001/openapi.json

## Endpoints Overview

### Tools (6 endpoints)

**POST /search** - Hybrid search (semantic + full-text)
```bash
curl -X POST http://localhost:8001/search \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "limit": 10}'
```

**POST /rag** - RAG generation with retrieval
```bash
curl -X POST http://localhost:8001/rag \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RAG?", "max_tokens": 4000}'
```

**POST /batch-analysis** - Analyze multiple documents
```bash
curl -X POST http://localhost:8001/batch-analysis \
  -H "Content-Type: application/json" \
  -d '{"document_ids": ["doc1", "doc2"], "analysis_type": "summary"}'
```

**POST /smart-search** - Collection-filtered search
```bash
curl -X POST http://localhost:8001/smart-search \
  -H "Content-Type: application/json" \
  -d '{"query": "AI", "collection_ids": ["col1"], "min_score": 0.7}'
```

**GET /stats** - Performance statistics
```bash
curl http://localhost:8001/stats
```

**POST /cache/clear** - Clear cache
```bash
curl -X POST http://localhost:8001/cache/clear
```

### Resources (4 endpoints)

**GET /resources/stats** - Server statistics
```bash
curl http://localhost:8001/resources/stats
```

**GET /resources/config** - Server configuration
```bash
curl http://localhost:8001/resources/config
```

**GET /resources/collection/{collection_id}** - Collection info
```bash
curl http://localhost:8001/resources/collection/abc123
```

**GET /resources/document/{document_id}** - Document summary
```bash
curl http://localhost:8001/resources/document/doc123
```

### Prompts (3 endpoints)

**POST /prompts/research** - Generate research prompt
```bash
curl -X POST http://localhost:8001/prompts/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "quantum computing", "depth": "comprehensive"}'
```

**POST /prompts/code-review** - Generate code review prompt
```bash
curl -X POST http://localhost:8001/prompts/code-review \
  -H "Content-Type: application/json" \
  -d '{
    "code_snippet": "def hello(): print(\"hi\")",
    "language": "python",
    "focus_areas": ["security", "performance"]
  }'
```

**POST /prompts/data-analysis** - Generate data analysis prompt
```bash
curl -X POST http://localhost:8001/prompts/data-analysis \
  -H "Content-Type: application/json" \
  -d '{"dataset_description": "Customer purchase history CSV with 100k rows"}'
```

### Misc (3 endpoints)

**GET /** - API info and endpoint list
**GET /health** - Health check
**GET /capabilities** - Full capabilities and features

## Request/Response Examples

### Search Example

**Request:**
```json
POST /search
{
  "query": "deep learning architectures",
  "limit": 5,
  "strategy": "hybrid"
}
```

**Response:**
```json
{
  "query": "deep learning architectures",
  "total_results": 5,
  "results": [
    {
      "text": "...",
      "score": 0.92,
      "metadata": {...}
    }
  ],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### RAG Example

**Request:**
```json
POST /rag
{
  "query": "Explain transformer architecture",
  "max_tokens": 2000
}
```

**Response:**
```json
{
  "query": "Explain transformer architecture",
  "answer": "Transformers are a neural network architecture...",
  "sources": [
    {
      "text": "...",
      "score": 0.95
    }
  ],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Features

✅ All MCP tools as REST endpoints
✅ All MCP resources as REST endpoints
✅ All MCP prompts as REST endpoints
✅ Automatic OpenAPI/Swagger documentation
✅ Request validation with Pydantic
✅ Async request handling
✅ CORS support
✅ Error handling with retry logic

## Architecture

```text
Client (curl/browser/app)
    ↓ HTTP REST
FastAPI Server (api.py:8001)
    ↓ HTTP JSON
R2R API (localhost:7272/v3/...)
    ↓
R2R Knowledge Base
```

## Comparison: MCP vs REST API

| Feature | MCP Server (server.py) | REST API (api.py) |
|---------|------------------------|-------------------|
| Protocol | stdio/SSE/WebSocket | HTTP REST |
| Client | Cursor/Claude Desktop | Any HTTP client |
| Context | Full Context support | Stateless |
| Progress | Real-time progress | HTTP responses |
| Middleware | Full stack | Basic |
| Use Case | IDE integration | Web/mobile apps |

## Development

### Run with auto-reload
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8001
```

### Test endpoint
```bash
# Health check
curl http://localhost:8001/health

# Capabilities
curl http://localhost:8001/capabilities

# Search test
curl -X POST http://localhost:8001/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "limit": 3}'
```

## Deployment

### Docker
```bash
# Build
docker build -t r2r-ultra-api -f Dockerfile.api .

# Run
docker run -p 8001:8001 \
  -e R2R_BASE_URL=http://r2r:7272 \
  -e API_KEY=your_key \
  r2r-ultra-api
```

### Systemd Service
```ini
[Unit]
Description=R2R Ultra API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/r2r-ultra-api
Environment="R2R_BASE_URL=http://localhost:7272"
Environment="API_KEY=your_key"
ExecStart=/opt/r2r-ultra-api/.venv/bin/uvicorn api:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```

## Configuration

Environment variables (`.env`):

```bash
# R2R Configuration (required)
R2R_BASE_URL=http://localhost:7272
API_KEY=your_r2r_api_key

# HTTP Client (optional)
TIMEOUT=120.0
MAX_RETRIES=3
```

## Error Handling

All endpoints return standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (resource doesn't exist)
- `500` - Server Error (R2R API issue)
- `503` - Service Unavailable (R2R not reachable)

Error response format:
```json
{
  "detail": "Error description"
}
```

## License

Same as R2R Ultra MCP Server project.
