#!/usr/bin/env python3
"""
FastAPI wrapper for R2R MCP Server tools.
Provides HTTP endpoints for testing MCP tools directly.
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load .env file
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if key not in os.environ:
                    os.environ[key] = value

# R2R Configuration
R2R_BASE_URL = os.getenv("R2R_BASE_URL", "http://localhost:7272")
API_KEY = os.getenv("API_KEY", "")
TIMEOUT = float(os.getenv("TIMEOUT", "120.0"))


def _get_headers() -> dict[str, str]:
    """Get authentication headers for R2R."""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers


async def _make_r2r_request(
    method: str,
    endpoint: str,
    data: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Make HTTP request to R2R."""
    url = f"{R2R_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        if method == "GET":
            response = await client.get(url, headers=_get_headers(), params=data or {})
        elif method == "POST":
            response = await client.post(url, headers=_get_headers(), json=data or {})
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()

# Create FastAPI app
app = FastAPI(
    title="R2R MCP Tools API",
    description="HTTP API for testing R2R MCP Server tools",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# Request/Response Models
# ========================================

class MockContext:
    """Mock Context for API calls (tools expect Context parameter)."""
    request_id = "api-request"
    client_id = "api-client"
    
    async def info(self, msg: str):
        print(f"ℹ️  {msg}")
    
    async def error(self, msg: str):
        print(f"❌ {msg}")
    
    async def warning(self, msg: str):
        print(f"⚠️  {msg}")
    
    async def report_progress(self, current: int, total: int, message: str):
        print(f"📊 Progress: {current}/{total} - {message}")


class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    strategy: str = "hybrid"


class RAGRequest(BaseModel):
    query: str
    max_tokens: int = 4000


class BatchDocumentAnalysisRequest(BaseModel):
    document_ids: list[str]
    analysis_type: str = "summary"


class SmartCollectionSearchRequest(BaseModel):
    query: str
    collection_ids: Optional[list[str]] = None
    min_score: float = 0.7


# ========================================
# API Endpoints
# ========================================

@app.get("/")
async def root():
    """API root - server info."""
    return {
        "name": "R2R MCP Tools API",
        "version": "3.0.0",
        "description": "REST API wrapper for R2R Ultra MCP Server - all MCP tools, resources, and prompts as HTTP endpoints",
        "r2r_base_url": R2R_BASE_URL,
        "api_key_configured": bool(API_KEY),
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        },
        "endpoints": {
            "tools": {
                "POST /search": "R2R search with progress",
                "POST /rag": "R2R RAG with sampling",
                "POST /batch-analysis": "Batch document analysis",
                "POST /smart-search": "Smart collection search",
                "GET /stats": "Performance statistics",
                "POST /cache/clear": "Clear cache"
            },
            "resources": {
                "GET /resources/stats": "Server statistics",
                "GET /resources/config": "Server configuration",
                "GET /resources/collection/{id}": "Collection info",
                "GET /resources/document/{id}": "Document summary"
            },
            "prompts": {
                "POST /prompts/research": "Research prompt generator",
                "POST /prompts/code-review": "Code review prompt",
                "POST /prompts/data-analysis": "Data analysis prompt"
            },
            "misc": {
                "GET /": "This info",
                "GET /health": "Health check",
                "GET /capabilities": "Server capabilities"
            }
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "r2r_base_url": R2R_BASE_URL,
        "api_key_configured": bool(API_KEY)
    }


@app.get("/capabilities")
async def capabilities():
    """Get server capabilities."""
    try:
        # Check R2R health
        health = await _make_r2r_request("GET", "/v3/health")

        return {
            "server": "R2R MCP Tools API",
            "version": "3.0.0",
            "r2r_base_url": R2R_BASE_URL,
            "r2r_health": health,
            "api_key_configured": bool(API_KEY),
            "features": {
                "search": True,
                "rag": True,
                "batch_analysis": True,
                "smart_search": True,
                "resources": True,
                "prompts": True,
                "cache_management": True
            },
            "endpoints": {
                "tools": [
                    "/search",
                    "/rag",
                    "/batch-analysis",
                    "/smart-search",
                    "/stats",
                    "/cache/clear"
                ],
                "resources": [
                    "/resources/stats",
                    "/resources/config",
                    "/resources/collection/{collection_id}",
                    "/resources/document/{document_id}"
                ],
                "prompts": [
                    "/prompts/research",
                    "/prompts/code-review",
                    "/prompts/data-analysis"
                ],
                "misc": [
                    "/",
                    "/health",
                    "/capabilities"
                ]
            },
            "endpoints_count": 16,
            "documentation": {
                "swagger_ui": "/docs",
                "redoc": "/redoc",
                "openapi_json": "/openapi.json"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search(request: SearchRequest):
    """R2R search with progress reporting."""
    try:
        payload = {
            "query": request.query,
            "limit": request.limit,
            "search_settings": {
                "use_hybrid_search": request.strategy == "hybrid",
                "search_strategy": request.strategy,
                "filters": {}
            }
        }
        
        result = await _make_r2r_request("POST", "/v3/retrieval/search", payload)
        
        return {
            "query": request.query,
            "strategy": request.strategy,
            "results": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rag")
async def rag(request: RAGRequest):
    """R2R RAG query with sampling."""
    try:
        payload = {
            "query": request.query,
            "search_settings": {
                "use_hybrid_search": True
            },
            "rag_generation_config": {
                "max_tokens_to_sample": request.max_tokens
            }
        }
        
        result = await _make_r2r_request("POST", "/v3/retrieval/rag", payload)
        
        return {
            "query": request.query,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch-analysis")
async def batch_analysis(request: BatchDocumentAnalysisRequest):
    """Analyze multiple documents in parallel."""
    try:
        results = []
        for doc_id in request.document_ids:
            try:
                doc = await _make_r2r_request("GET", f"/v3/documents/{doc_id}")
                doc_data = doc.get("results", {})
                results.append({
                    "id": doc_id,
                    "title": doc_data.get("title", "Untitled"),
                    "status": doc_data.get("ingestion_status"),
                    "size": doc_data.get("size_in_bytes", 0)
                })
            except Exception as e:
                results.append({"id": doc_id, "error": str(e)})
        
        return {
            "analysis_type": request.analysis_type,
            "total_documents": len(request.document_ids),
            "successful": sum(1 for r in results if "error" not in r),
            "failed": sum(1 for r in results if "error" in r),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/smart-search")
async def smart_search(request: SmartCollectionSearchRequest):
    """Smart collection search with filtering."""
    try:
        search_settings = {
            "use_hybrid_search": True,
            "search_strategy": "hybrid",
            "filters": {}
        }
        
        if request.collection_ids:
            search_settings["filters"]["collection_ids"] = {"$overlap": request.collection_ids}
        
        payload = {
            "query": request.query,
            "limit": 20,
            "search_settings": search_settings
        }
        
        result = await _make_r2r_request("POST", "/v3/retrieval/search", payload)
        
        # Filter by score
        results = result.get("results", {}).get("chunk_search_results", [])
        filtered = [r for r in results if r.get("score", 0) >= request.min_score]
        
        return {
            "query": request.query,
            "total_found": len(results),
            "after_filtering": len(filtered),
            "min_score": request.min_score,
            "collections": request.collection_ids or [],
            "results": filtered[:10],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def stats():
    """Get performance statistics (mock data for API)."""
    return {
        "timestamp": datetime.now().isoformat(),
        "api_uptime": "N/A (stateless API)",
        "r2r_url": R2R_BASE_URL,
        "api_key_configured": bool(API_KEY)
    }


@app.post("/cache/clear")
async def clear_cache_endpoint():
    """Clear cache (not applicable for stateless API)."""
    return {
        "status": "info",
        "message": "Stateless API - no cache to clear",
        "timestamp": datetime.now().isoformat()
    }


# ========================================
# Resources Endpoints
# ========================================

@app.get("/resources/stats")
async def server_stats_resource():
    """Get R2R server statistics."""
    try:
        collections = await _make_r2r_request("GET", "/v3/collections")
        health = await _make_r2r_request("GET", "/v3/health")

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "collections_count": len(collections.get("results", [])),
            "r2r_health": health,
            "uptime": "N/A (stateless API)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/resources/config")
async def server_config_resource():
    """Get server configuration."""
    return {
        "r2r_base_url": R2R_BASE_URL,
        "api_version": "3.0.0",
        "api_key_configured": bool(API_KEY),
        "timeout": TIMEOUT,
        "features": {
            "hybrid_search": True,
            "rag_generation": True,
            "collections": True,
            "knowledge_graph": True,
            "batch_analysis": True
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/resources/collection/{collection_id}")
async def collection_info_resource(collection_id: str):
    """Get detailed collection information."""
    try:
        collection = await _make_r2r_request("GET", f"/v3/collections/{collection_id}")
        return {
            "status": "success",
            "collection": collection,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Collection not found: {str(e)}")


@app.get("/resources/document/{document_id}")
async def document_summary_resource(document_id: str):
    """Get document summary and metadata."""
    try:
        document = await _make_r2r_request("GET", f"/v3/documents/{document_id}")
        return {
            "status": "success",
            "document_id": document_id,
            "title": document.get("title", "Untitled"),
            "summary": document.get("summary", "No summary available"),
            "metadata": document.get("metadata", {}),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Document not found: {str(e)}")


# ========================================
# Prompts Endpoints
# ========================================

class ResearchPromptRequest(BaseModel):
    """Research prompt request."""
    topic: str
    depth: str = "standard"  # quick, standard, comprehensive


class CodeReviewRequest(BaseModel):
    """Code review prompt request."""
    code_snippet: str
    language: str = "python"
    focus_areas: list[str] = ["security", "performance", "best_practices"]


class DataAnalysisRequest(BaseModel):
    """Data analysis prompt request."""
    dataset_description: str


@app.post("/prompts/research")
async def research_prompt(request: ResearchPromptRequest):
    """Generate research question prompt."""
    depth_instructions = {
        "quick": "Provide a concise overview focusing on key points only.",
        "standard": "Provide a balanced analysis covering main aspects and implications.",
        "comprehensive": "Conduct thorough research covering all aspects, implications, and related topics."
    }

    instruction = depth_instructions.get(request.depth, depth_instructions["standard"])

    prompt = f"""Research Topic: {request.topic}

Depth Level: {request.depth}

Instructions:
{instruction}

Please structure your response with:
1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Implications
5. Recommendations
6. Sources/References
"""

    return {
        "role": "user",
        "content": prompt,
        "metadata": {
            "topic": request.topic,
            "depth": request.depth
        },
        "timestamp": datetime.now().isoformat()
    }


@app.post("/prompts/code-review")
async def code_review_prompt(request: CodeReviewRequest):
    """Generate code review prompt."""
    focus_areas_text = "\n".join([f"- {area}" for area in request.focus_areas])

    prompt = f"""Code Review Request

Language: {request.language}

Focus Areas:
{focus_areas_text}

Code to Review:
```{request.language}
{request.code_snippet}
```

Please provide a comprehensive code review covering:
1. Code Quality & Readability
2. Security Vulnerabilities
3. Performance Optimization Opportunities
4. Best Practices Compliance
5. Specific Recommendations for Improvement

Format your review with clear sections and actionable feedback.
"""

    return {
        "role": "user",
        "content": prompt,
        "metadata": {
            "language": request.language,
            "focus_areas": request.focus_areas
        },
        "timestamp": datetime.now().isoformat()
    }


@app.post("/prompts/data-analysis")
async def data_analysis_prompt(request: DataAnalysisRequest):
    """Generate data analysis prompt."""
    prompt = f"""Data Analysis Request

Dataset: {request.dataset_description}

Please perform the following analysis:

1. Data Overview
   - Describe the dataset structure and key variables
   - Identify data types and formats

2. Exploratory Analysis
   - Summary statistics
   - Distribution analysis
   - Missing data assessment

3. Key Insights
   - Patterns and trends
   - Correlations and relationships
   - Anomalies or outliers

4. Visualization Recommendations
   - Suggest appropriate chart types
   - Key metrics to visualize

5. Analysis Recommendations
   - Statistical methods to apply
   - Further investigation areas

Please provide specific, actionable insights based on the dataset characteristics.
"""

    return {
        "role": "user",
        "content": prompt,
        "metadata": {
            "dataset_description": request.dataset_description
        },
        "timestamp": datetime.now().isoformat()
    }


# ========================================
# Run Server
# ========================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 R2R MCP Tools API Server")
    print("=" * 60)
    print(f"📡 R2R URL: {R2R_BASE_URL}")
    print(f"🔑 API Key: {'Configured' if API_KEY else 'Not configured'}")
    print("=" * 60)
    print("📖 API Documentation: http://localhost:8001/docs")
    print("🔍 Interactive UI: http://localhost:8001/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
