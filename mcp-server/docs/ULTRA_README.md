# 🚀 R2R Ultra FastMCP Server v3.0

**Production-ready MCP server with ALL advanced FastMCP features.**

Enterprise-grade R2R integration server showcasing the full power of FastMCP framework with middleware, lifespan management, context integration, resources, prompts, and best practices for production deployment.

---

## ✨ Features

### 🔧 **Middleware Architecture** (5 Types)

1. **LoggingMiddleware** - Comprehensive request/response logging
   - Automatic request numbering
   - Timing information
   - Error tracking
   
2. **TimingMiddleware** - Performance monitoring
   - Per-operation timing
   - Average time calculation
   - Operation call counting
   
3. **RateLimitingMiddleware** - Abuse prevention
   - Per-client rate limiting
   - Configurable limits
   - Automatic cleanup
   
4. **ErrorHandlingMiddleware** - Intelligent error handling
   - Automatic retry with exponential backoff
   - Error statistics tracking
   - Graceful degradation
   
5. **CachingMiddleware** - Performance optimization
   - In-memory result caching
   - TTL-based expiration
   - Hit/miss tracking

### 🔄 **Lifespan Management**

- Automatic startup/shutdown hooks
- R2R connectivity verification
- Resource initialization
- Statistics tracking
- Graceful cleanup

### 📊 **Context Integration**

- **Progress Reporting** - Real-time operation updates
- **Structured Logging** - Debug, info, warning, error levels
- **LLM Sampling** - Request text generation from client's LLM
- **Request Metadata** - Access session ID, request ID, etc.
- **Resource Access** - Read resources from within tools

### 📚 **Resources & Templates**

- **Static Resources** - Server stats, configuration
- **Dynamic Resources** - Collection info, document summaries
- **Parameterized Templates** - URI placeholders map to function parameters
- **Context-Aware** - Logging and error handling built-in

### 🎯 **Reusable Prompts**

- **Research Questions** - Standard and deep research templates
- **Code Review** - Multiple focus areas (security, performance, readability)
- **Data Analysis** - Structured analysis prompts
- **Context Integration** - Prompts can use Context for metadata

### 🏗️ **Production-Ready Patterns**

- Environment variable configuration
- Comprehensive error handling
- Performance monitoring
- Security best practices
- Scalable architecture

---

## 📦 Installation

### Prerequisites

```bash
# Python 3.10+
python --version

# Install dependencies
pip install fastmcp httpx
```

### Environment Setup

Create `.env` file:

```bash
# Required
R2R_BASE_URL=http://localhost:7272

# Optional but recommended
API_KEY=your_r2r_api_key_here

# Advanced configuration
MAX_RETRIES=3
TIMEOUT=120.0
```

---

## 🚀 Quick Start

### 1. Basic Usage

```bash
# Run the server (stdio transport)
python server_ultra.py

# Or with FastMCP CLI
fastmcp run server_ultra.py
```

### 2. HTTP/SSE Transport

```python
# In your code
mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

```bash
# Or via CLI
fastmcp run server_ultra.py --transport sse --port 8000
```

### 3. With MCP Client

```python
from fastmcp import Client
import asyncio

async def main():
    async with Client("http://localhost:8000/sse") as client:
        # Get server capabilities
        result = await client.call_tool(
            "get_server_capabilities",
            arguments={}
        )
        print(result)
        
        # Search with progress
        result = await client.call_tool(
            "r2r_search_with_progress",
            arguments={"query": "machine learning", "limit": 5}
        )
        print(result)

asyncio.run(main())
```

---

## 🎯 Tool Categories

### 📊 Server Information

#### `get_server_capabilities()`
Get comprehensive server status and capabilities.

```python
{
    "server": "R2R Ultra MCP Server",
    "version": "3.0.0",
    "features": {
        "middleware": [...],
        "lifespan_management": true,
        "context_integration": true
    },
    "statistics": {
        "timing": {...},
        "cache": {...}
    }
}
```

#### `get_performance_stats()`
Get detailed performance metrics from middleware.

```python
{
    "timing": {
        "operations": ["search", "rag"],
        "total_calls": 1250,
        "average_times": {"search": 145.5}
    },
    "cache": {
        "hits": 450,
        "misses": 800,
        "hit_rate": "36.0%"
    }
}
```

### 🔍 Search Tools

#### `r2r_search_with_progress(query, limit, strategy, ctx)`
Advanced search with real-time progress reporting.

**Features:**
- Progress updates (0%, 30%, 100%)
- Context logging
- Multiple strategies (hybrid, hyde, rag_fusion)
- Automatic caching
- Rate limiting

**Example:**
```python
result = await client.call_tool(
    "r2r_search_with_progress",
    arguments={
        "query": "artificial intelligence",
        "limit": 10,
        "strategy": "hybrid"
    }
)
```

**Progress Output:**
```
📊 [0%] Initializing search
📊 [30%] Sending search request
📊 [100%] Search completed
✅ Found 15 results
```

### 💬 RAG Tools

#### `r2r_rag_with_sampling(query, max_tokens, ctx)`
RAG query with optional LLM sampling.

**Features:**
- Context-aware generation
- Progress reporting
- Automatic caching
- Error handling with retry

**Example:**
```python
result = await client.call_tool(
    "r2r_rag_with_sampling",
    arguments={
        "query": "Explain quantum computing",
        "max_tokens": 4000
    }
)
```

### 📊 Batch Operations

#### `batch_document_analysis(document_ids, analysis_type, ctx)`
Analyze multiple documents with progress tracking.

**Features:**
- Parallel processing
- Real-time progress (1/10, 2/10, ...)
- Error handling per document
- Summary statistics

**Example:**
```python
result = await client.call_tool(
    "batch_document_analysis",
    arguments={
        "document_ids": ["doc1", "doc2", "doc3"],
        "analysis_type": "summary"
    }
)

# Returns:
{
    "total_documents": 3,
    "successful": 2,
    "failed": 1,
    "results": [...]
}
```

### 🔍 Smart Search

#### `smart_collection_search(query, collection_ids, min_score, ctx)`
Intelligent search with automatic filtering.

**Features:**
- Automatic score filtering
- Collection-specific search
- Result ranking
- Statistics

**Example:**
```python
result = await client.call_tool(
    "smart_collection_search",
    arguments={
        "query": "machine learning",
        "collection_ids": ["coll1", "coll2"],
        "min_score": 0.7
    }
)

# Returns:
{
    "total_found": 25,
    "after_filtering": 12,
    "results": [...]
}
```

### 🧹 Utility Tools

#### `clear_cache()`
Clear server cache and reset statistics.

**Example:**
```python
result = await client.call_tool("clear_cache", arguments={})

# Returns:
{
    "status": "success",
    "message": "Cache cleared (120 entries removed)"
}
```

---

## 📚 Resources

### Static Resources

#### `r2r://server/stats`
Real-time server statistics.

```python
resource = await client.read_resource("r2r://server/stats")
# Returns JSON with server status, uptime, R2R URL
```

#### `r2r://config`
Server configuration.

```python
resource = await client.read_resource("r2r://config")
# Returns configuration including API settings
```

### Resource Templates (Parameterized)

#### `r2r://collection/{collection_id}/info`
Collection information by ID.

```python
resource = await client.read_resource("r2r://collection/abc123/info")
# Returns collection details
```

#### `r2r://document/{document_id}/summary`
Document summary by ID.

```python
resource = await client.read_resource("r2r://document/doc456/summary")
# Returns document summary with metadata
```

---

## 🎨 Prompts

### Research Question Prompt

```python
prompt = await client.get_prompt(
    "research_question_prompt",
    arguments={
        "topic": "artificial intelligence",
        "depth": "deep"  # or "standard"
    }
)
```

**Depth Options:**
- `standard` - Concise overview
- `deep` - Comprehensive analysis with background, challenges, future directions

### Code Review Prompt

```python
prompt = await client.get_prompt(
    "code_review_prompt",
    arguments={
        "code_snippet": "def add(a, b): return a + b",
        "language": "python",
        "focus": "security"  # or "performance", "readability", "general"
    }
)
```

### Data Analysis Prompt

```python
prompt = await client.get_prompt(
    "data_analysis_prompt",
    arguments={
        "dataset_description": "Sales data for Q4 2024"
    }
)
```

---

## 🔧 Configuration

### Middleware Configuration

```python
# Customize in server_ultra.py

# Logging - All requests
mcp.add_middleware(LoggingMiddleware())

# Timing - Performance monitoring
mcp.add_middleware(TimingMiddleware())

# Rate limiting - 100 requests/minute per client
mcp.add_middleware(RateLimitingMiddleware(max_requests_per_minute=100))

# Error handling - 2 retries with backoff
mcp.add_middleware(ErrorHandlingMiddleware(max_retries=2))

# Caching - 5 minute TTL
mcp.add_middleware(CachingMiddleware(ttl=300))
```

### Lifespan Configuration

```python
@asynccontextmanager
async def server_lifespan(app):
    # Startup
    logger.info("Starting up...")
    # Initialize resources
    
    yield {"stats": server_stats}
    
    # Shutdown
    logger.info("Shutting down...")
    # Cleanup resources
```

---

## 📊 Monitoring

### Real-time Logs

```bash
2024-01-15 10:30:45 - mcp.logging - INFO - 📨 [1] tools/call from stdio
2024-01-15 10:30:45 - mcp.timing - INFO - ⏱️ Tool 'search' executed in 145.50ms (avg: 145.50ms, calls: 1)
2024-01-15 10:30:45 - mcp.cache - INFO - 📝 Cache MISS for 'search:...'
2024-01-15 10:30:45 - mcp.logging - INFO - ✅ [1] tools/call completed in 150.23ms
```

### Performance Metrics

```python
# Get detailed statistics
stats = await client.call_tool("get_performance_stats", arguments={})

print(f"Cache hit rate: {stats['cache']['hit_rate']}")
print(f"Average search time: {stats['timing']['average_times']['search']}ms")
print(f"Total errors: {stats['errors']['total_errors']}")
```

### Error Tracking

```python
# Errors are automatically tracked by ErrorHandlingMiddleware
stats = await get_performance_stats()

print(stats['errors']['errors_by_type'])
# Output:
{
    "search:HTTP500": 5,
    "rag:TimeoutError": 3,
    "agent:ConnectionError": 15
}
```

---

## 🎓 Usage Patterns

### Pattern 1: Simple Tool Call

```python
# No context needed for simple operations
result = await client.call_tool(
    "get_server_capabilities",
    arguments={}
)
```

### Pattern 2: Tool with Progress

```python
# Tools automatically report progress when Context is used
result = await client.call_tool(
    "r2r_search_with_progress",
    arguments={"query": "AI", "limit": 10}
)

# Server automatically logs:
# 📊 [0%] Initializing search
# 📊 [30%] Sending search request
# 📊 [100%] Search completed
```

### Pattern 3: Batch Processing

```python
# Process multiple items with progress
result = await client.call_tool(
    "batch_document_analysis",
    arguments={
        "document_ids": ["doc1", "doc2", "doc3", "doc4", "doc5"],
        "analysis_type": "summary"
    }
)

# Server logs progress for each document:
# 📊 [1/5] Processing document 1/5
# 📊 [2/5] Processing document 2/5
# ...
```

### Pattern 4: Using Resources

```python
# Read static resource
stats = await client.read_resource("r2r://server/stats")

# Read parameterized resource
collection = await client.read_resource("r2r://collection/abc123/info")
document = await client.read_resource("r2r://document/doc456/summary")
```

### Pattern 5: Using Prompts

```python
# Get research prompt
prompt = await client.get_prompt(
    "research_question_prompt",
    arguments={"topic": "quantum computing", "depth": "deep"}
)

# Use prompt with LLM
response = await llm.generate(prompt.messages)
```

---

## 🔒 Security Best Practices

### 1. API Key Management

```bash
# NEVER commit API keys
# Use environment variables
export API_KEY=your_secret_key_here

# Or use .env file (add to .gitignore)
echo "API_KEY=your_secret_key_here" > .env
```

### 2. Rate Limiting

```python
# Configure appropriate limits
mcp.add_middleware(
    RateLimitingMiddleware(max_requests_per_minute=60)
)
```

### 3. Error Handling

```python
# Never expose internal errors to clients
class ErrorHandlingMiddleware(Middleware):
    async def on_call_tool(self, context, call_next):
        try:
            return await call_next(context)
        except Exception as e:
            # Log internally
            logger.error(f"Internal error: {e}")
            # Return safe message
            raise McpError(ErrorData(
                code=-32603,
                message="An internal error occurred"
            ))
```

### 4. Input Validation

```python
@mcp.tool()
async def secure_tool(query: str, limit: int = 10) -> Dict[str, Any]:
    """Tool with input validation."""
    # Validate inputs
    if not query or len(query) > 1000:
        raise ValueError("Query must be 1-1000 characters")
    
    if limit < 1 or limit > 100:
        raise ValueError("Limit must be 1-100")
    
    # Process safely
    return await process(query, limit)
```

---

## 🚀 Deployment

### Local Development

```bash
# Development with stdio
python server_ultra.py

# Development with HTTP/SSE
fastmcp run server_ultra.py --transport sse --port 8000
```

### Production (Docker)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server_ultra.py .

ENV R2R_BASE_URL=http://r2r:7272
ENV API_KEY=${R2R_API_KEY}

CMD ["python", "server_ultra.py"]
```

```bash
# Build
docker build -t r2r-mcp-ultra .

# Run
docker run -e R2R_BASE_URL=http://your-r2r:7272 \
           -e API_KEY=your_key \
           -p 8000:8000 \
           r2r-mcp-ultra
```

### Production (Systemd)

```ini
[Unit]
Description=R2R Ultra MCP Server
After=network.target

[Service]
Type=simple
User=mcp
WorkingDirectory=/opt/r2r-mcp
Environment="R2R_BASE_URL=http://localhost:7272"
Environment="API_KEY=your_key_here"
ExecStart=/usr/bin/python3 /opt/r2r-mcp/server_ultra.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 📈 Performance Tuning

### 1. Cache Configuration

```python
# Longer TTL for stable data
mcp.add_middleware(CachingMiddleware(ttl=3600))  # 1 hour

# Shorter TTL for dynamic data
mcp.add_middleware(CachingMiddleware(ttl=60))  # 1 minute
```

### 2. Rate Limiting

```python
# High traffic
mcp.add_middleware(RateLimitingMiddleware(max_requests_per_minute=1000))

# Low traffic / strict limits
mcp.add_middleware(RateLimitingMiddleware(max_requests_per_minute=10))
```

### 3. Retry Strategy

```python
# Aggressive retries
mcp.add_middleware(ErrorHandlingMiddleware(max_retries=5))

# Conservative retries
mcp.add_middleware(ErrorHandlingMiddleware(max_retries=1))
```

### 4. Timeout Configuration

```bash
# For slow R2R instances
export TIMEOUT=300.0

# For fast R2R instances
export TIMEOUT=30.0
```

---

## 🐛 Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Check Middleware Statistics

```python
# Get detailed stats
stats = await client.call_tool("get_performance_stats", arguments={})

# Check for issues
if stats['errors']['total_errors'] > 0:
    print("Errors detected:", stats['errors']['errors_by_type'])

if float(stats['cache']['hit_rate'].rstrip('%')) < 20:
    print("Low cache hit rate!")
```

### Monitor Tool Execution

```bash
# Watch logs in real-time
tail -f mcp-server.log | grep "⏱️"

# Example output:
# ⏱️ Tool 'search' executed in 145.50ms (avg: 145.50ms, calls: 1)
# ⏱️ Tool 'rag' executed in 2100.30ms (avg: 2100.30ms, calls: 1)
```

---

## 🎯 Best Practices

### 1. Always Use Context

```python
@mcp.tool()
async def my_tool(query: str, ctx: Context = None) -> Dict[str, Any]:
    """Tool with context integration."""
    if ctx:
        await ctx.info(f"Processing: {query}")
        await ctx.report_progress(0, 100, "Starting")
    
    # Your code here
    
    if ctx:
        await ctx.report_progress(100, 100, "Complete")
    
    return result
```

### 2. Report Progress for Long Operations

```python
async def long_operation(items: List[str], ctx: Context = None):
    """Report progress for batch operations."""
    total = len(items)
    
    for idx, item in enumerate(items):
        if ctx:
            await ctx.report_progress(idx + 1, total, f"Processing {idx + 1}/{total}")
        
        # Process item
        await process(item)
```

### 3. Use Resources for Read-Only Data

```python
# Good - Use resource
@mcp.resource("r2r://stats")
async def get_stats() -> str:
    return json.dumps({"key": "value"})

# Avoid - Use tool for read-only data
@mcp.tool()
async def get_stats() -> Dict[str, Any]:
    return {"key": "value"}
```

### 4. Create Reusable Prompts

```python
# Good - Parameterized prompt
@mcp.prompt()
async def analysis_prompt(topic: str, depth: str = "standard"):
    return [UserMessage(content=f"Analyze {topic} ({depth})")]

# Avoid - Hard-coded prompt
@mcp.prompt()
async def ai_prompt():
    return [UserMessage(content="Analyze AI")]
```

### 5. Implement Proper Error Handling

```python
@mcp.tool()
async def safe_tool(query: str, ctx: Context = None) -> Dict[str, Any]:
    """Tool with comprehensive error handling."""
    try:
        # Validate input
        if not query:
            raise ValueError("Query cannot be empty")
        
        # Process
        result = await process(query)
        
        return {"status": "success", "result": result}
        
    except ValueError as e:
        if ctx:
            await ctx.error(f"Validation error: {e}")
        raise McpError(ErrorData(code=-32602, message=str(e)))
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Unexpected error: {e}")
        raise McpError(ErrorData(code=-32603, message="Internal error"))
```

---

## 📚 Additional Resources

- [R2R Documentation](https://r2r-docs.sciphi.ai/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP Middleware Guide](https://gofastmcp.com/servers/middleware)
- [FastMCP Context Guide](https://gofastmcp.com/servers/context)
- [FastMCP Resources Guide](https://gofastmcp.com/servers/resources)
- [FastMCP Prompts Guide](https://gofastmcp.com/servers/prompts)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Follow the existing code style
2. Add comprehensive docstrings
3. Include type hints
4. Update documentation
5. Add tests for new features

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **R2R Team** - For the amazing RAG framework
- **FastMCP Team** - For the excellent MCP framework
- **Anthropic** - For the Model Context Protocol specification

---

**Made with 💙 by R2R MCP Team**

*Version 3.0.0 - Production Ready* 🚀

