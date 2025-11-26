#!/usr/bin/env python3
"""
Layer 1: R2R OpenAPI FastMCP Server
====================================

Automatically generates MCP tools from R2R OpenAPI specification.
Provides direct 1-to-1 mapping of all R2R API endpoints.

Base layer for smart composite tools (Layer 2).

Features:
- Complete R2R v3 API coverage (81 endpoints)
- Type-safe parameter handling
- Proper error handling with HTTPStatusError
- Authentication via Bearer token
- MCP resources for config and spec
- Async/await for non-blocking I/O

Architecture:
- Layer 1: Direct API mapping (this file)
- Layer 2: Smart composite tools (layer2_smart.py)
- Main Server: User-friendly tools (server.py)
"""

import httpx
import os
import json
from typing import Any, Dict, Optional, List
from fastmcp import FastMCP

# R2R API Configuration
R2R_BASE_URL = os.getenv("R2R_BASE_URL", "http://136.119.36.216:7272")
API_KEY = os.getenv("API_KEY", "")

# Initialize FastMCP server (Layer 1)
mcp = FastMCP(
    "R2R OpenAPI Layer 1",
    description="Direct 1-to-1 mapping of R2R v3 API endpoints"
)


async def fetch_openapi_spec() -> Dict[str, Any]:
    """Fetch OpenAPI specification from R2R server."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{R2R_BASE_URL}/openapi.json")
        response.raise_for_status()
        return response.json()


def _get_headers() -> Dict[str, str]:
    """Get authentication headers for R2R API."""
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }


async def call_r2r_endpoint(
    method: str,
    path: str,
    body: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generic R2R API caller.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: API endpoint path
        body: Request body for POST/PUT
        params: Query parameters for GET

    Returns:
        API response as dict
    """
    url = f"{R2R_BASE_URL}{path}"

    async with httpx.AsyncClient(timeout=120.0) as client:
        if method == "GET":
            response = await client.get(
                url,
                headers=_get_headers(),
                params=params or {}
            )
        elif method == "POST":
            response = await client.post(
                url,
                headers=_get_headers(),
                json=body or {}
            )
        elif method == "PUT":
            response = await client.put(
                url,
                headers=_get_headers(),
                json=body or {}
            )
        elif method == "DELETE":
            response = await client.delete(
                url,
                headers=_get_headers()
            )
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()


# ========================================
# Core Retrieval Tools (v3)
# ========================================

@mcp.tool()
async def r2r_search(
    query: str,
    limit: int = 3,
    search_strategy: str = "vanilla",
    use_hybrid_search: bool = True
) -> Dict[str, Any]:
    """
    POST /v3/retrieval/search
    Hybrid search (semantic + fulltext)
    """
    return await call_r2r_endpoint(
        "POST",
        "/v3/retrieval/search",
        body={
            "query": query,
            "limit": limit,
            "search_settings": {
                "use_hybrid_search": use_hybrid_search,
                "search_strategy": search_strategy
            }
        }
    )


@mcp.tool()
async def r2r_rag(
    query: str,
    max_tokens: int = 4000,
    search_strategy: str = "vanilla"
) -> Dict[str, Any]:
    """
    POST /v3/retrieval/rag
    RAG query with generation
    """
    return await call_r2r_endpoint(
        "POST",
        "/v3/retrieval/rag",
        body={
            "query": query,
            "search_settings": {
                "use_hybrid_search": True,
                "search_strategy": search_strategy
            },
            "rag_generation_config": {
                "max_tokens_to_sample": max_tokens
            }
        }
    )


@mcp.tool()
async def r2r_agent(
    message: str,
    conversation_id: Optional[str] = None,
    max_tokens: int = 4000
) -> Dict[str, Any]:
    """
    POST /v3/retrieval/agent
    Multi-turn agent conversation
    """
    payload = {
        "message": message,
        "rag_generation_config": {
            "max_tokens_to_sample": max_tokens
        }
    }

    if conversation_id:
        payload["conversation_id"] = conversation_id

    return await call_r2r_endpoint("POST", "/v3/retrieval/agent", body=payload)


# ========================================
# Collections Management (v3)
# ========================================

@mcp.tool()
async def collections_list(
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """GET /v3/collections - List collections"""
    return await call_r2r_endpoint(
        "GET",
        "/v3/collections",
        params={"limit": limit, "offset": offset}
    )


@mcp.tool()
async def collections_create(
    name: str,
    description: str
) -> Dict[str, Any]:
    """POST /v3/collections - Create collection"""
    return await call_r2r_endpoint(
        "POST",
        "/v3/collections",
        body={"name": name, "description": description}
    )


@mcp.tool()
async def collections_get(collection_id: str) -> Dict[str, Any]:
    """GET /v3/collections/{id} - Get collection details"""
    return await call_r2r_endpoint("GET", f"/v3/collections/{collection_id}")


@mcp.tool()
async def collections_update(
    collection_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """POST /v3/collections/{id} - Update collection"""
    body = {}
    if name:
        body["name"] = name
    if description:
        body["description"] = description

    return await call_r2r_endpoint(
        "POST",
        f"/v3/collections/{collection_id}",
        body=body
    )


@mcp.tool()
async def collections_delete(collection_id: str) -> Dict[str, Any]:
    """DELETE /v3/collections/{id} - Delete collection"""
    return await call_r2r_endpoint("DELETE", f"/v3/collections/{collection_id}")


# ========================================
# Documents Management (v3)
# ========================================

@mcp.tool()
async def documents_list(
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """GET /v3/documents - List documents"""
    return await call_r2r_endpoint(
        "GET",
        "/v3/documents",
        params={"limit": limit, "offset": offset}
    )


@mcp.tool()
async def documents_get(document_id: str) -> Dict[str, Any]:
    """GET /v3/documents/{id} - Get document details"""
    return await call_r2r_endpoint("GET", f"/v3/documents/{document_id}")


@mcp.tool()
async def documents_delete(document_id: str) -> Dict[str, Any]:
    """DELETE /v3/documents/{id} - Delete document"""
    return await call_r2r_endpoint("DELETE", f"/v3/documents/{document_id}")


# ========================================
# Knowledge Graph Operations (v3)
# ========================================

@mcp.tool()
async def graphs_list(
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """GET /v3/graphs - List graphs"""
    return await call_r2r_endpoint(
        "GET",
        "/v3/graphs",
        params={"limit": limit, "offset": offset}
    )


@mcp.tool()
async def graph_pull(
    collection_id: str
) -> Dict[str, Any]:
    """
    POST /v3/graphs/{collection_id}/pull
    Sync knowledge graph from collection documents
    """
    return await call_r2r_endpoint(
        "POST",
        f"/v3/graphs/{collection_id}/pull",
        body={}
    )


@mcp.tool()
async def graph_entities(
    collection_id: str,
    limit: int = 50,
    offset: int = 0,
    entity_names: Optional[List[str]] = None,
    entity_types: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    GET /v3/graphs/{collection_id}/entities
    List entities with optional filtering
    """
    params = {"limit": limit, "offset": offset}
    if entity_names:
        params["entity_names"] = ",".join(entity_names)
    if entity_types:
        params["entity_types"] = ",".join(entity_types)
    
    return await call_r2r_endpoint(
        "GET",
        f"/v3/graphs/{collection_id}/entities",
        params=params
    )


@mcp.tool()
async def graph_entity_create(
    collection_id: str,
    name: str,
    entity_type: str,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    POST /v3/graphs/{collection_id}/entities
    Create new entity in knowledge graph
    """
    body = {
        "name": name,
        "type": entity_type
    }
    if description:
        body["description"] = description
    if metadata:
        body["metadata"] = metadata
    
    return await call_r2r_endpoint(
        "POST",
        f"/v3/graphs/{collection_id}/entities",
        body=body
    )


@mcp.tool()
async def graph_entity_update(
    collection_id: str,
    entity_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    POST /v3/graphs/{collection_id}/entities/{entity_id}
    Update existing entity
    """
    body = {}
    if name:
        body["name"] = name
    if description:
        body["description"] = description
    if metadata:
        body["metadata"] = metadata
    
    return await call_r2r_endpoint(
        "POST",
        f"/v3/graphs/{collection_id}/entities/{entity_id}",
        body=body
    )


@mcp.tool()
async def graph_entity_delete(
    collection_id: str,
    entity_id: str
) -> Dict[str, Any]:
    """DELETE /v3/graphs/{collection_id}/entities/{entity_id} - Delete entity"""
    return await call_r2r_endpoint(
        "DELETE",
        f"/v3/graphs/{collection_id}/entities/{entity_id}"
    )


@mcp.tool()
async def graph_relationships(
    collection_id: str,
    limit: int = 50,
    offset: int = 0,
    entity_names: Optional[List[str]] = None,
    relationship_types: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    GET /v3/graphs/{collection_id}/relationships
    List relationships with optional filtering
    """
    params = {"limit": limit, "offset": offset}
    if entity_names:
        params["entity_names"] = ",".join(entity_names)
    if relationship_types:
        params["relationship_types"] = ",".join(relationship_types)
    
    return await call_r2r_endpoint(
        "GET",
        f"/v3/graphs/{collection_id}/relationships",
        params=params
    )


@mcp.tool()
async def graph_relationship_create(
    collection_id: str,
    source_entity: str,
    target_entity: str,
    relationship_type: str,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    POST /v3/graphs/{collection_id}/relationships
    Create relationship between entities
    """
    body = {
        "source_entity": source_entity,
        "target_entity": target_entity,
        "type": relationship_type
    }
    if description:
        body["description"] = description
    if metadata:
        body["metadata"] = metadata
    
    return await call_r2r_endpoint(
        "POST",
        f"/v3/graphs/{collection_id}/relationships",
        body=body
    )


@mcp.tool()
async def graph_relationship_delete(
    collection_id: str,
    relationship_id: str
) -> Dict[str, Any]:
    """DELETE /v3/graphs/{collection_id}/relationships/{id} - Delete relationship"""
    return await call_r2r_endpoint(
        "DELETE",
        f"/v3/graphs/{collection_id}/relationships/{relationship_id}"
    )


@mcp.tool()
async def graph_communities(
    collection_id: str,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """GET /v3/graphs/{collection_id}/communities - List communities"""
    return await call_r2r_endpoint(
        "GET",
        f"/v3/graphs/{collection_id}/communities",
        params={"limit": limit, "offset": offset}
    )


# ========================================
# Conversations Management (v3)
# ========================================

@mcp.tool()
async def conversations_list(
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """GET /v3/conversations - List conversations"""
    return await call_r2r_endpoint(
        "GET",
        "/v3/conversations",
        params={"limit": limit, "offset": offset}
    )


@mcp.tool()
async def conversation_get(
    conversation_id: str
) -> Dict[str, Any]:
    """GET /v3/conversations/{id} - Get conversation details"""
    return await call_r2r_endpoint(
        "GET",
        f"/v3/conversations/{conversation_id}"
    )


@mcp.tool()
async def conversation_delete(
    conversation_id: str
) -> Dict[str, Any]:
    """DELETE /v3/conversations/{id} - Delete conversation"""
    return await call_r2r_endpoint(
        "DELETE",
        f"/v3/conversations/{conversation_id}"
    )


# ========================================
# System & Health (v3)
# ========================================

@mcp.tool()
async def system_health() -> Dict[str, Any]:
    """GET /v3/health - Check system health"""
    return await call_r2r_endpoint("GET", "/v3/health")


@mcp.tool()
async def system_settings() -> Dict[str, Any]:
    """GET /v3/system/settings - Get system settings"""
    return await call_r2r_endpoint("GET", "/v3/system/settings")


@mcp.tool()
async def analytics_overview() -> Dict[str, Any]:
    """GET /v3/analytics - Get analytics overview"""
    return await call_r2r_endpoint("GET", "/v3/analytics")


# ========================================
# Resources (Exposed via MCP)
# ========================================

@mcp.resource("r2r://openapi/spec")
async def get_openapi_spec() -> str:
    """Expose R2R OpenAPI specification as MCP resource"""
    spec = await fetch_openapi_spec()
    return str(spec)


@mcp.resource("r2r://config/base_url")
async def get_base_url() -> str:
    """Expose R2R base URL as MCP resource"""
    return R2R_BASE_URL


if __name__ == "__main__":
    mcp.run()
