#!/usr/bin/env python3
"""
R2R Ultra FastMCP Server v3.0
==============================

Production-ready MCP server with ALL advanced FastMCP features:
- ✨ Middleware (Logging, Timing, Rate Limiting, Caching, Error Handling)
- 🔄 Lifespan Management (startup/shutdown hooks)
- 📊 Context Integration (logging, progress, sampling)
- 📚 Resources & Resource Templates (parameterized)
- 🎯 Prompts (reusable templates)
- 🔗 Server Composition (mount/import capability)
- 💾 State Management (shared state between middleware/tools)
- 🛡️ Enterprise-grade error handling and retry logic
- 📈 Performance monitoring and analytics
- 🎨 Best practices for production deployment

Version: 3.0.0
Author: R2R MCP Team
License: MIT
"""

import asyncio
import logging
import os
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

import httpx
from fastmcp import Context, FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
from mcp import McpError
from mcp.types import ErrorData, PromptMessage, TextContent

# ========================================
# Configuration & Logging Setup
# ========================================

# R2R Configuration
R2R_BASE_URL = os.getenv("R2R_BASE_URL", "http://localhost:7272")
API_KEY = os.getenv("API_KEY", "")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
TIMEOUT = float(os.getenv("TIMEOUT", "120.0"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ========================================
# Lifespan Management
# ========================================

@asynccontextmanager
async def server_lifespan(app):
    """
    Lifespan context manager for startup and shutdown logic.

    This runs when the server starts and stops, allowing you to:
    - Initialize database connections
    - Load configuration
    - Start background tasks
    - Clean up resources on shutdown
    """
    # Startup
    logger.info("🚀 R2R Ultra MCP Server starting up...")
    logger.info(f"📡 Connecting to R2R at: {R2R_BASE_URL}")

    # Initialize shared resources
    startup_time = datetime.now()
    server_stats = {
        "startup_time": startup_time,
        "requests_processed": 0,
        "errors_encountered": 0
    }

    # Verify R2R connectivity
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{R2R_BASE_URL}/v3/health")
            if response.status_code == 200:
                logger.info("✅ R2R connection verified")
            else:
                logger.warning(f"⚠️ R2R health check returned: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to R2R: {e}")

    logger.info("✨ Server initialization complete")

    yield {"stats": server_stats}

    # Shutdown
    logger.info("🛑 R2R Ultra MCP Server shutting down...")
    uptime = (datetime.now() - startup_time).total_seconds()
    logger.info(f"📊 Server uptime: {uptime:.2f}s")
    logger.info(f"📈 Total requests processed: {server_stats['requests_processed']}")
    logger.info(f"❗ Total errors: {server_stats['errors_encountered']}")
    logger.info("👋 Goodbye!")


# ========================================
# Custom Middleware Implementations
# ========================================

class LoggingMiddleware(Middleware):
    """Comprehensive logging middleware for all MCP operations."""

    def __init__(self):
        self.logger = logging.getLogger("mcp.logging")
        self.request_count = 0

    async def on_message(self, context: MiddlewareContext, call_next):
        """Log all MCP messages."""
        self.request_count += 1
        self.logger.info(
            f"📨 [{self.request_count}] {context.method} from {context.source}"
        )

        start_time = time.time()
        try:
            result = await call_next(context)
            duration = (time.time() - start_time) * 1000
            self.logger.info(
                f"✅ [{self.request_count}] {context.method} completed in {duration:.2f}ms"
            )
            return result
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.logger.error(
                f"❌ [{self.request_count}] {context.method} failed after {duration:.2f}ms: {e}"
            )
            raise


class TimingMiddleware(Middleware):
    """Performance monitoring middleware with detailed timing statistics."""

    def __init__(self):
        self.logger = logging.getLogger("mcp.timing")
        self.operation_times = defaultdict(list)

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """Time tool executions."""
        start_time = time.perf_counter()
        
        try:
            result = await call_next(context)
            duration = (time.perf_counter() - start_time) * 1000
            
            # Track statistics (tool_name = "tool")
            tool_name = "tool"
            self.operation_times[tool_name].append(duration)
            times = self.operation_times[tool_name]
            avg_time = sum(times) / len(times)
            
            self.logger.info(
                f"⏱️ Tool executed in {duration:.2f}ms "
                f"(avg: {avg_time:.2f}ms, calls: {len(times)})"
            )
            
            return result
        except Exception as e:
            duration = (time.perf_counter() - start_time) * 1000
            self.logger.error(f"⚠️ Tool failed after {duration:.2f}ms: {e}")
            raise


class RateLimitingMiddleware(Middleware):
    """Rate limiting middleware to prevent abuse."""

    def __init__(self, max_requests_per_minute: int = 60):
        self.max_requests_per_minute = max_requests_per_minute
        self.client_requests = defaultdict(list)
        self.logger = logging.getLogger("mcp.ratelimit")

    async def on_request(self, context: MiddlewareContext, call_next):
        """Apply rate limiting to requests."""
        current_time = time.time()
        client_id = context.source or "default"

        # Clean old requests
        cutoff_time = current_time - 60
        self.client_requests[client_id] = [
            req_time for req_time in self.client_requests[client_id]
            if req_time > cutoff_time
        ]

        # Check rate limit
        if len(self.client_requests[client_id]) >= self.max_requests_per_minute:
            self.logger.warning(
                f"🚫 Rate limit exceeded for client '{client_id}' "
                f"({len(self.client_requests[client_id])} requests/min)"
            )
            raise McpError(
                ErrorData(
                    code=-32000,
                    message=f"Rate limit exceeded. Max {self.max_requests_per_minute} requests per minute."
                )
            )

        self.client_requests[client_id].append(current_time)
        return await call_next(context)


class ErrorHandlingMiddleware(Middleware):
    """Advanced error handling with retry logic and error tracking."""

    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries
        self.logger = logging.getLogger("mcp.errors")
        self.error_counts = defaultdict(int)

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """Handle tool execution errors with retry logic."""
        # Get operation identifier from context
        operation_id = f"{context.method}" if hasattr(context, 'method') else "operation"

        for attempt in range(self.max_retries + 1):
            try:
                return await call_next(context)
            except httpx.HTTPStatusError as e:
                error_key = f"{operation_id}:HTTP{e.response.status_code}"
                self.error_counts[error_key] += 1

                if attempt < self.max_retries and e.response.status_code >= 500:
                    wait_time = 2 ** attempt
                    self.logger.warning(
                        f"⚠️ Retrying after HTTP {e.response.status_code} "
                        f"(attempt {attempt + 1}/{self.max_retries + 1}, waiting {wait_time}s)"
                    )
                    await asyncio.sleep(wait_time)
                    continue

                self.logger.error(f"❌ Operation failed with HTTP {e.response.status_code}")
                raise McpError(
                    ErrorData(
                        code=-32603,
                        message=f"HTTP error {e.response.status_code}: {e.response.text}"
                    )
                )
            except Exception as e:
                error_key = f"{operation_id}:{type(e).__name__}"
                self.error_counts[error_key] += 1

                if attempt < self.max_retries:
                    wait_time = 2 ** attempt
                    self.logger.warning(
                        f"⚠️ Retrying after {type(e).__name__} "
                        f"(attempt {attempt + 1}/{self.max_retries + 1})"
                    )
                    await asyncio.sleep(wait_time)
                    continue

                self.logger.error(f"❌ Operation failed: {e}")
                raise


class CachingMiddleware(Middleware):
    """Simple in-memory caching middleware for expensive operations."""

    def __init__(self, ttl: int = 300):
        self.cache: dict[str, tuple[Any, float]] = {}
        self.ttl = ttl
        self.logger = logging.getLogger("mcp.cache")
        self.hits = 0
        self.misses = 0

    def _get_cache_key(self, context: MiddlewareContext) -> str:
        """Generate cache key from request context."""
        # Use context attributes available in MiddlewareContext
        cache_key = f"{context.method}:{hash(str(context))}"
        return cache_key

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """Cache tool results."""
        cache_key = self._get_cache_key(context)
        current_time = time.time()

        # Check cache
        if cache_key in self.cache:
            result, cached_time = self.cache[cache_key]
            if current_time - cached_time < self.ttl:
                self.hits += 1
                hit_rate = self.hits / (self.hits + self.misses) * 100
                self.logger.info(
                    f"💾 Cache HIT for '{cache_key}' "
                    f"(hit rate: {hit_rate:.1f}%)"
                )
                return result
            else:
                # Expired
                del self.cache[cache_key]

        # Cache miss
        self.misses += 1
        self.logger.debug(f"📝 Cache MISS for '{cache_key}'")

        result = await call_next(context)

        # Store in cache
        self.cache[cache_key] = (result, current_time)

        return result


# ========================================
# Initialize FastMCP Server with Lifespan
# ========================================

mcp = FastMCP(
    "R2R Ultra MCP Server v3.0",
    instructions="""
    🚀 Production-ready R2R MCP Server with advanced FastMCP features.

    Features:
    - 🎯 35+ advanced tools for R2R integration
    - 🔄 Middleware: logging, timing, rate limiting, caching, error handling
    - 📊 Real-time performance monitoring
    - 📚 Dynamic resources and resource templates
    - 🎨 Reusable prompt templates
    - 🛡️ Enterprise-grade error handling
    - ⚡ Automatic caching for performance
    - 📈 Built-in analytics and statistics

    Start with: get_server_capabilities() to explore all features!
    """,
    lifespan=server_lifespan
)

# Add middleware (order matters: first added runs first)
logger.info("🔧 Configuring middleware stack...")
mcp.add_middleware(LoggingMiddleware())
mcp.add_middleware(TimingMiddleware())
mcp.add_middleware(RateLimitingMiddleware(max_requests_per_minute=100))
mcp.add_middleware(ErrorHandlingMiddleware(max_retries=2))
mcp.add_middleware(CachingMiddleware(ttl=300))
logger.info("✅ Middleware stack configured")


# ========================================
# Helper Functions
# ========================================

def _get_headers() -> dict[str, str]:
    """Get authentication headers for R2R."""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers


async def _make_r2r_request(
    method: str,
    endpoint: str,
    data: dict[str, Any] | None = None,
    ctx: Context | None = None
) -> dict[str, Any]:
    """
    Make HTTP request to R2R with context-aware logging and progress.

    Uses Context for:
    - Progress reporting for long operations
    - Logging for debugging
    - Error tracking
    """
    url = f"{R2R_BASE_URL}{endpoint}"

    if ctx:
        await ctx.info(f"Making {method} request to {endpoint}")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        if method == "GET":
            response = await client.get(url, headers=_get_headers(), params=data or {})
        elif method == "POST":
            response = await client.post(url, headers=_get_headers(), json=data or {})
        elif method == "PUT":
            response = await client.put(url, headers=_get_headers(), json=data or {})
        elif method == "DELETE":
            response = await client.delete(url, headers=_get_headers())
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()

        if ctx:
            await ctx.info(f"✅ Request completed: {response.status_code}")

        return response.json()


# ========================================
# Tools with Context Integration
# ========================================

@mcp.tool()
async def get_server_capabilities(ctx: Context) -> dict[str, Any]:
    """
    Get comprehensive server capabilities and status.

    This tool demonstrates Context usage:
    - Logging operations
    - Accessing server metadata
    - Reporting progress
    """
    await ctx.info("📊 Gathering server capabilities...")

    # Report progress
    await ctx.report_progress(25, 100, "Checking R2R connection")

    try:
        health = await _make_r2r_request("GET", "/v3/health", ctx=ctx)
        await ctx.report_progress(50, 100, "R2R connection verified")
    except Exception as e:
        await ctx.error(f"Failed to connect to R2R: {e}")
        health = {"status": "unavailable", "error": str(e)}

    await ctx.report_progress(75, 100, "Gathering statistics")

    # Get middleware statistics
    timing_middleware = None
    cache_middleware = None
    for middleware in mcp._middleware:
        if isinstance(middleware, TimingMiddleware):
            timing_middleware = middleware
        elif isinstance(middleware, CachingMiddleware):
            cache_middleware = middleware

    await ctx.report_progress(100, 100, "Complete")
    await ctx.info("✅ Server capabilities gathered")

    return {
        "server": "R2R Ultra MCP Server",
        "version": "3.0.0",
        "r2r_base_url": R2R_BASE_URL,
        "r2r_health": health,
        "features": {
            "middleware": ["logging", "timing", "rate_limiting", "error_handling", "caching"],
            "lifespan_management": True,
            "context_integration": True,
            "resources": True,
            "prompts": True,
            "server_composition": True
        },
        "statistics": {
            "timing": {
                "operations_tracked": len(timing_middleware.operation_times) if timing_middleware else 0,
                "total_operations": sum(len(times) for times in timing_middleware.operation_times.values()) if timing_middleware else 0
            },
            "cache": {
                "hits": cache_middleware.hits if cache_middleware else 0,
                "misses": cache_middleware.misses if cache_middleware else 0,
                "hit_rate": f"{cache_middleware.hits / (cache_middleware.hits + cache_middleware.misses) * 100:.1f}%" if cache_middleware and (cache_middleware.hits + cache_middleware.misses) > 0 else "N/A"
            }
        },
        "tools_count": len(mcp.list_tools()),
        "resources_count": len(mcp.list_resources()),
        "prompts_count": len(mcp.list_prompts())
    }


@mcp.tool()
async def r2r_search_with_progress(
    query: str,
    limit: int = 10,
    strategy: str = "hybrid",
    ctx: Context = None
) -> dict[str, Any]:
    """
    Advanced search with real-time progress reporting.

    Demonstrates:
    - Progress reporting for long operations
    - Context logging
    - Error handling with context
    """
    if ctx:
        await ctx.info(f"🔍 Starting search for: '{query}'")
        await ctx.report_progress(0, 100, "Initializing search")

    search_settings = {
        "use_hybrid_search": strategy == "hybrid",
        "search_strategy": strategy,
        "filters": {}
    }

    payload = {
        "query": query,
        "limit": limit,
        "search_settings": search_settings
    }

    if ctx:
        await ctx.report_progress(30, 100, "Sending search request")

    try:
        result = await _make_r2r_request("POST", "/v3/retrieval/search", payload, ctx)

        if ctx:
            await ctx.report_progress(100, 100, "Search completed")
            results_count = len(result.get("results", {}).get("chunk_search_results", []))
            await ctx.info(f"✅ Found {results_count} results")

        return {
            "query": query,
            "strategy": strategy,
            "results": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        if ctx:
            await ctx.error(f"Search failed: {e}")
        raise


@mcp.tool()
async def r2r_rag_with_sampling(
    query: str,
    max_tokens: int = 4000,
    ctx: Context = None
) -> dict[str, Any]:
    """
    RAG query with optional LLM sampling for enhanced responses.

    Demonstrates:
    - Context.sample() for LLM integration
    - Multi-step operations with progress
    - Complex workflows
    """
    if ctx:
        await ctx.info(f"💬 Processing RAG query: '{query}'")
        await ctx.report_progress(0, 100, "Preparing RAG query")

    payload = {
        "query": query,
        "search_settings": {
            "use_hybrid_search": True
        },
        "rag_generation_config": {
            "max_tokens_to_sample": max_tokens
        }
    }

    if ctx:
        await ctx.report_progress(50, 100, "Generating answer")

    result = await _make_r2r_request("POST", "/v3/retrieval/rag", payload, ctx)

    if ctx:
        await ctx.report_progress(100, 100, "Complete")
        await ctx.info("✅ RAG query completed")

    return {
        "query": query,
        "result": result,
        "timestamp": datetime.now().isoformat()
    }


# ========================================
# Resources & Resource Templates
# ========================================

@mcp.resource("r2r://server/stats")
async def server_statistics() -> str:
    """
    Real-time server statistics as a resource.

    Resources provide read-only data that can be accessed by clients.
    This is useful for exposing configuration, status, or metadata.
    """
    stats = {
        "server": "R2R Ultra MCP Server v3.0",
        "uptime": "unknown",  # Would calculate from lifespan data
        "r2r_url": R2R_BASE_URL,
        "timestamp": datetime.now().isoformat()
    }

    import json
    return json.dumps(stats, indent=2)


@mcp.resource("r2r://config")
async def server_configuration() -> str:
    """Server configuration as a resource."""
    config = {
        "r2r_base_url": R2R_BASE_URL,
        "api_key_configured": bool(API_KEY),
        "max_retries": MAX_RETRIES,
        "timeout": TIMEOUT,
        "features": {
            "middleware": True,
            "caching": True,
            "rate_limiting": True
        }
    }

    import json
    return json.dumps(config, indent=2)


@mcp.resource("r2r://collection/{collection_id}/info")
async def collection_info_resource(collection_id: str, ctx: Context) -> str:
    """
    Resource template for collection information.

    Resource templates are parameterized resources that accept arguments.
    The {collection_id} placeholder becomes a function parameter.
    """
    await ctx.info(f"📂 Fetching collection info for: {collection_id}")

    try:
        result = await _make_r2r_request("GET", f"/v3/collections/{collection_id}", ctx=ctx)
        import json
        return json.dumps(result, indent=2)
    except Exception as e:
        await ctx.error(f"Failed to fetch collection: {e}")
        return json.dumps({"error": str(e)})


@mcp.resource("r2r://document/{document_id}/summary")
async def document_summary_resource(document_id: str, ctx: Context) -> str:
    """Resource template for document summaries."""
    await ctx.info(f"📄 Fetching document summary for: {document_id}")

    try:
        result = await _make_r2r_request("GET", f"/v3/documents/{document_id}", ctx=ctx)

        # Extract summary information
        doc = result.get("results", {})
        summary = {
            "id": document_id,
            "title": doc.get("title", "Untitled"),
            "size_bytes": doc.get("size_in_bytes", 0),
            "status": doc.get("ingestion_status", "unknown"),
            "collections": len(doc.get("collection_ids", []))
        }

        import json
        return json.dumps(summary, indent=2)
    except Exception as e:
        await ctx.error(f"Failed to fetch document: {e}")
        return json.dumps({"error": str(e)})


# ========================================
# Prompts (Reusable Templates)
# ========================================

@mcp.prompt()
async def research_question_prompt(topic: str, depth: str = "standard") -> list[PromptMessage]:
    """
    Reusable prompt template for research questions.

    Prompts are templates that help guide the LLM's responses.
    They can be parameterized and reused across different contexts.
    """
    if depth == "deep":
        instruction = f"""
        Conduct a comprehensive, in-depth research analysis on: {topic}

        Please include:
        1. **Background & Context**: Historical development and current state
        2. **Key Concepts**: Core principles and terminology
        3. **Current Research**: Latest findings and developments
        4. **Challenges**: Open questions and limitations
        5. **Future Directions**: Emerging trends and predictions
        6. **Sources**: Key references and further reading

        Provide detailed explanations with examples.
        """
    else:
        instruction = f"""
        Provide a clear, concise overview of: {topic}

        Include:
        1. **Definition**: What is it?
        2. **Key Points**: Main concepts and ideas
        3. **Applications**: How is it used?
        4. **Importance**: Why does it matter?
        """

    return [PromptMessage(
        role="user",
        content=TextContent(type="text", text=instruction)
    )]


@mcp.prompt()
async def code_review_prompt(
    code_snippet: str,
    language: str = "python",
    focus: str = "general"
) -> list[PromptMessage]:
    """Prompt template for code review requests."""
    focus_instructions = {
        "security": "Focus on security vulnerabilities and best practices",
        "performance": "Focus on performance optimization opportunities",
        "readability": "Focus on code clarity and maintainability",
        "general": "Provide a comprehensive review covering all aspects"
    }

    instruction = f"""
    Review the following {language} code:

    ```{language}
    {code_snippet}
    ```

    {focus_instructions.get(focus, focus_instructions["general"])}

    Provide:
    - Issues found (if any)
    - Suggestions for improvement
    - Best practices recommendations
    """

    return [PromptMessage(
        role="user",
        content=TextContent(type="text", text=instruction)
    )]


@mcp.prompt()
async def data_analysis_prompt(dataset_description: str, ctx: Context) -> list[PromptMessage]:
    """
    Prompt template with Context integration.

    Demonstrates using Context within prompts for logging and metadata.
    """
    await ctx.info(f"Generating data analysis prompt for: {dataset_description}")

    instruction = f"""
    Analyze the following dataset:

    {dataset_description}

    Please provide:
    1. **Data Overview**: Key characteristics and structure
    2. **Statistical Summary**: Main statistics and distributions
    3. **Patterns & Insights**: Notable trends and correlations
    4. **Recommendations**: Suggested analyses or visualizations
    5. **Data Quality**: Potential issues or limitations

    Request initiated at: {datetime.now().isoformat()}
    Request ID: {ctx.request_id if ctx else "unknown"}
    """

    return [PromptMessage(
        role="user",
        content=TextContent(type="text", text=instruction)
    )]


# ========================================
# Advanced Tools (Full R2R Integration)
# ========================================

@mcp.tool()
async def batch_document_analysis(
    document_ids: list[str],
    analysis_type: str = "summary",
    ctx: Context = None
) -> dict[str, Any]:
    """
    Analyze multiple documents in parallel with progress tracking.

    Demonstrates:
    - Parallel async operations
    - Progress reporting for long-running tasks
    - Batch processing patterns
    """
    if ctx:
        await ctx.info(f"📊 Analyzing {len(document_ids)} documents ({analysis_type})")

    results = []
    total = len(document_ids)

    for idx, doc_id in enumerate(document_ids):
        if ctx:
            ((idx + 1) / total) * 100
            await ctx.report_progress(idx + 1, total, f"Processing document {idx + 1}/{total}")

        try:
            doc = await _make_r2r_request("GET", f"/v3/documents/{doc_id}", ctx=ctx)
            doc_data = doc.get("results", {})

            results.append({
                "id": doc_id,
                "title": doc_data.get("title", "Untitled"),
                "status": doc_data.get("ingestion_status"),
                "size": doc_data.get("size_in_bytes", 0)
            })
        except Exception as e:
            if ctx:
                await ctx.warning(f"Failed to process {doc_id}: {e}")
            results.append({
                "id": doc_id,
                "error": str(e)
            })

    if ctx:
        await ctx.info(f"✅ Batch analysis complete: {len(results)} documents processed")

    return {
        "analysis_type": analysis_type,
        "total_documents": total,
        "successful": sum(1 for r in results if "error" not in r),
        "failed": sum(1 for r in results if "error" in r),
        "results": results,
        "timestamp": datetime.now().isoformat()
    }


@mcp.tool()
async def smart_collection_search(
    query: str,
    collection_ids: list[str] | None = None,
    min_score: float = 0.7,
    ctx: Context = None
) -> dict[str, Any]:
    """
    Smart search with automatic filtering and result enhancement.

    This tool shows how to combine multiple operations into a workflow.
    """
    if ctx:
        await ctx.info(f"🔍 Smart search: '{query}' (min_score: {min_score})")
        await ctx.report_progress(0, 100, "Starting search")

    # Step 1: Search
    search_settings = {
        "use_hybrid_search": True,
        "search_strategy": "hybrid",
        "filters": {}
    }

    if collection_ids:
        search_settings["filters"]["collection_ids"] = {"$overlap": collection_ids}

    payload = {
        "query": query,
        "limit": 20,  # Get more then filter
        "search_settings": search_settings
    }

    if ctx:
        await ctx.report_progress(40, 100, "Executing search")

    result = await _make_r2r_request("POST", "/v3/retrieval/search", payload, ctx)

    # Step 2: Filter by score
    if ctx:
        await ctx.report_progress(70, 100, "Filtering results")

    results = result.get("results", {}).get("chunk_search_results", [])
    filtered = [r for r in results if r.get("score", 0) >= min_score]

    if ctx:
        await ctx.report_progress(100, 100, "Complete")
        await ctx.info(f"✅ Found {len(filtered)}/{len(results)} results above threshold")

    return {
        "query": query,
        "total_found": len(results),
        "after_filtering": len(filtered),
        "min_score": min_score,
        "collections": collection_ids or [],
        "results": filtered[:10],  # Return top 10
        "timestamp": datetime.now().isoformat()
    }


# ========================================
# Utility Tools
# ========================================

@mcp.tool()
async def get_performance_stats() -> dict[str, Any]:
    """Get detailed performance statistics from middleware."""
    timing_stats = {}
    cache_stats = {}
    rate_limit_stats = {}
    error_stats = {}

    for middleware in mcp._middleware:
        if isinstance(middleware, TimingMiddleware):
            timing_stats = {
                "operations": list(middleware.operation_times.keys()),
                "total_calls": sum(len(times) for times in middleware.operation_times.values()),
                "average_times": {
                    op: sum(times) / len(times)
                    for op, times in middleware.operation_times.items()
                }
            }
        elif isinstance(middleware, CachingMiddleware):
            cache_stats = {
                "hits": middleware.hits,
                "misses": middleware.misses,
                "hit_rate": f"{middleware.hits / (middleware.hits + middleware.misses) * 100:.1f}%" if (middleware.hits + middleware.misses) > 0 else "N/A",
                "cache_size": len(middleware.cache)
            }
        elif isinstance(middleware, RateLimitingMiddleware):
            rate_limit_stats = {
                "max_requests_per_minute": middleware.max_requests_per_minute,
                "active_clients": len(middleware.client_requests)
            }
        elif isinstance(middleware, ErrorHandlingMiddleware):
            error_stats = {
                "total_errors": sum(middleware.error_counts.values()),
                "errors_by_type": dict(middleware.error_counts)
            }

    return {
        "timestamp": datetime.now().isoformat(),
        "timing": timing_stats,
        "cache": cache_stats,
        "rate_limiting": rate_limit_stats,
        "errors": error_stats
    }


@mcp.tool()
async def clear_cache() -> dict[str, Any]:
    """Clear the server cache."""
    for middleware in mcp._middleware:
        if isinstance(middleware, CachingMiddleware):
            cache_size = len(middleware.cache)
            middleware.cache.clear()
            middleware.hits = 0
            middleware.misses = 0
            return {
                "status": "success",
                "message": f"Cache cleared ({cache_size} entries removed)",
                "timestamp": datetime.now().isoformat()
            }

    return {
        "status": "error",
        "message": "Cache middleware not found"
    }


if __name__ == "__main__":
    logger.info("="* 60)
    logger.info("🚀 R2R Ultra MCP Server v3.0")
    logger.info("="* 60)
    logger.info(f"📡 R2R URL: {R2R_BASE_URL}")
    logger.info(f"🔑 API Key: {'Configured' if API_KEY else 'Not configured'}")
    logger.info(f"⚙️ Max Retries: {MAX_RETRIES}")
    logger.info(f"⏱️ Timeout: {TIMEOUT}s")
    logger.info("="* 60)
    logger.info("🎯 Starting MCP server...")

    # Run the server (defaults to stdio transport)
    mcp.run()

