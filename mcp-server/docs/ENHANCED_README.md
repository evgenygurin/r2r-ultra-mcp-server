# R2R Enhanced FastMCP Server v2.0

🚀 Production-ready MCP server with advanced R2R capabilities including knowledge graphs, streaming, advanced search strategies, and comprehensive monitoring.

## ✨ New Features in v2.0

### 🔍 Advanced Search
- **Multiple Strategies**: Hybrid, HyDE, RAG-Fusion
- **Knowledge Graph Integration**: Include KG context in search results
- **Semantic Comparison**: Compare texts using vector similarity
- **Batch Search**: Process multiple queries in parallel

### 🧠 Knowledge Graph
- **Extraction**: Automatic entity and relationship extraction from documents
- **Querying**: Natural language graph queries
- **Entity Management**: Create, update, and delete entities
- **Relationship Mapping**: Define and query relationships between entities

### 💬 Enhanced Conversations
- **Multi-turn Memory**: Context retention across conversations
- **Extended Thinking**: Deep reasoning with Claude's thinking tokens
- **Conversation Management**: List, get, delete, and export conversations
- **Research Mode**: Multi-step analysis with reasoning traces

### 📊 Monitoring & Analytics
- **System Health**: Real-time health checks and diagnostics
- **Analytics Overview**: Usage statistics and metrics
- **Collection Stats**: Detailed analytics per collection
- **Document Analytics**: Comprehensive document insights

### 🔄 Streaming Support
- **RAG Streaming**: Real-time response generation
- **Agent Streaming**: Streaming conversation responses
- **Progress Tracking**: Track long-running operations

### 📝 Document Management
- **Metadata Updates**: Update document metadata without re-uploading
- **Advanced Filtering**: Filter documents by collections and metadata
- **Detailed Information**: Get comprehensive document details
- **Batch Operations**: Process multiple documents efficiently

## 🎯 Quick Start

### 1. Installation

```bash
# Install dependencies
uv pip install -e .

# Or with pip
pip install -e .
```

### 2. Configuration

Create `.env` file:

```bash
R2R_BASE_URL=http://localhost:7272  # Your R2R instance URL
API_KEY=your_api_key_here            # R2R API key
MAX_RETRIES=3                        # Maximum retry attempts
TIMEOUT=120.0                        # Request timeout in seconds
```

### 3. Run Server

```bash
# Run enhanced server
python server_enhanced.py

# Or with fastmcp CLI
fastmcp run server_enhanced.py
```

### 4. Configure in Claude Code

Add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "r2r-enhanced": {
      "command": "python",
      "args": ["/path/to/server_enhanced.py"],
      "env": {
        "R2R_BASE_URL": "http://localhost:7272",
        "API_KEY": "your_api_key",
        "MAX_RETRIES": "3",
        "TIMEOUT": "120.0"
      }
    }
  }
}
```

## 📚 Usage Guide

### Getting Started

```python
# 1. Check server capabilities
capabilities = await get_server_info()

# 2. Verify connection
health = await system_health()

# 3. Explore available tools
help = await explain_capabilities()
```

### Advanced Search Examples

#### Hybrid Search (Best for most cases)
```python
results = await r2r_search_advanced(
    query="machine learning algorithms",
    limit=10,
    strategy="hybrid"
)
```

#### HyDE Search (Good for conceptual queries)
```python
results = await r2r_search_advanced(
    query="explain transformer architecture",
    limit=10,
    strategy="hyde"
)
```

#### RAG-Fusion (Comprehensive coverage)
```python
results = await r2r_search_advanced(
    query="quantum computing applications",
    limit=20,
    strategy="rag_fusion",
    use_kg=True  # Include knowledge graph context
)
```

#### Semantic Comparison
```python
comparison = await r2r_search_semantic_compare(
    text_a="Artificial Intelligence",
    text_b="Machine Learning",
    threshold=0.7
)
```

### RAG with Extended Context

```python
# Standard RAG
answer = await r2r_rag_extended(
    query="What are the benefits of RAG?",
    max_tokens=8000,
    search_limit=20
)

# RAG with web search
answer = await r2r_rag_extended(
    query="Latest advances in AI",
    max_tokens=8000,
    enable_web_search=True
)

# Streaming RAG (requires SSE transport)
stream = await r2r_rag_stream(
    query="Explain knowledge graphs",
    strategy="hybrid"
)
```

### Agent with Extended Thinking

```python
# Start research conversation
response = await r2r_agent_extended(
    message="Research the impact of quantum computing on cryptography",
    mode="research",
    enable_thinking=True,
    thinking_budget=4096
)

conversation_id = response["conversation_id"]

# Follow-up with context
follow_up = await r2r_agent_extended(
    message="What are the specific vulnerabilities?",
    conversation_id=conversation_id,
    mode="research"
)

# View conversation history
history = await conv_get(conversation_id)
```

### Knowledge Graph Operations

#### Extract Knowledge Graph
```python
graph = await graph_extract(
    document_id="doc_abc123",
    entity_types=["Person", "Organization", "Technology"],
    relationship_types=["WORKS_FOR", "USES", "DEVELOPS"]
)
```

#### Query Knowledge Graph
```python
results = await graph_query(
    collection_id="coll_xyz789",
    query="What technologies does OpenAI use?",
    entity_types=["Technology"]
)
```

#### Create Entities and Relationships
```python
# Create entity
entity = await graph_entities_create(
    collection_id="coll_xyz789",
    name="GPT-4",
    entity_type="Technology",
    description="Large Language Model",
    metadata={"version": "4", "release_year": 2023}
)

# Create relationship
relationship = await graph_relationships_create(
    collection_id="coll_xyz789",
    source_entity="OpenAI",
    target_entity="GPT-4",
    relationship_type="DEVELOPS",
    description="OpenAI develops GPT-4"
)
```

### Document Management

#### Update Metadata
```python
updated = await doc_update_metadata(
    document_id="doc_abc123",
    metadata={
        "category": "research",
        "tags": ["AI", "ML", "NLP"],
        "priority": "high",
        "reviewed": True
    }
)
```

#### List with Filters
```python
documents = await doc_list_with_filters(
    limit=50,
    collection_ids=["coll_xyz789"],
    metadata_filter={"category": "research"}
)
```

#### Get Detailed Information
```python
details = await doc_get_details(document_id="doc_abc123")
```

### Collection Management

#### Create Smart Collection
```python
collection = await collection_create_smart(
    name="AI Research Papers",
    description="Collection of AI research papers and articles",
    tags=["AI", "Research", "Academic"],
    metadata={
        "year": 2024,
        "source": "arxiv",
        "language": "en"
    }
)
```

#### Get Collection Statistics
```python
stats = await collection_stats(collection_id="coll_xyz789")

# Returns:
# {
#     "document_count": 42,
#     "total_size_bytes": 1048576,
#     "has_knowledge_graph": True,
#     "health": {
#         "status": "healthy",
#         "ingestion_complete": True
#     }
# }
```

### Monitoring & Analytics

#### System Health
```python
health = await system_health()

# Returns:
# {
#     "status": "healthy",
#     "r2r_base_url": "http://localhost:7272",
#     "health_check": {...},
#     "server_info": {
#         "version": "2.0.0",
#         "max_retries": 3
#     }
# }
```

#### Analytics Overview
```python
analytics = await analytics_overview()

# Returns:
# {
#     "counts": {
#         "documents": 150,
#         "collections": 5,
#         "conversations": 23
#     },
#     "timestamp": "2024-11-26T..."
# }
```

### Batch Operations

#### Batch Search
```python
results = await batch_search(
    queries=[
        "machine learning",
        "deep learning",
        "neural networks"
    ],
    limit_per_query=5,
    strategy="hybrid"
)
```

## 🔧 Advanced Configuration

### Environment Variables

```bash
# Core Configuration
R2R_BASE_URL=http://localhost:7272    # R2R API base URL
API_KEY=your_api_key                  # Authentication token

# Performance
MAX_RETRIES=3                         # Maximum retry attempts
TIMEOUT=120.0                         # Request timeout (seconds)

# MCP Server
FASTMCP_SERVER_NAME="R2R Enhanced"    # Server name
FASTMCP_SERVER_PORT=8000              # Port for HTTP transport
```

### Custom Configuration

Create `config.py`:

```python
import os

class Config:
    R2R_BASE_URL = os.getenv("R2R_BASE_URL", "http://localhost:7272")
    API_KEY = os.getenv("API_KEY", "")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT = float(os.getenv("TIMEOUT", "120.0"))
    
    # Search defaults
    DEFAULT_SEARCH_STRATEGY = "hybrid"
    DEFAULT_SEARCH_LIMIT = 10
    
    # RAG defaults
    DEFAULT_RAG_TOKENS = 4000
    DEFAULT_THINKING_BUDGET = 4096
    
    # KG defaults
    DEFAULT_ENTITY_TYPES = ["Person", "Organization", "Technology"]
```

## 🎨 Tool Categories

### 1. Search & Discovery (5 tools)
- `r2r_search_advanced` - Multi-strategy search
- `r2r_search_semantic_compare` - Text similarity
- `batch_search` - Parallel queries

### 2. RAG & Generation (2 tools)
- `r2r_rag_stream` - Streaming RAG
- `r2r_rag_extended` - Extended context RAG

### 3. Agent & Conversations (4 tools)
- `r2r_agent_extended` - Extended thinking agent
- `conv_list` - List conversations
- `conv_get` - Get conversation details
- `conv_delete` - Delete conversation

### 4. Knowledge Graph (4 tools)
- `graph_extract` - Extract KG from documents
- `graph_query` - Query knowledge graph
- `graph_entities_create` - Create entities
- `graph_relationships_create` - Create relationships

### 5. Document Management (3 tools)
- `doc_update_metadata` - Update metadata
- `doc_get_details` - Get document info
- `doc_list_with_filters` - Advanced filtering

### 6. Collection Management (2 tools)
- `collection_create_smart` - Create with metadata
- `collection_stats` - Get statistics

### 7. Monitoring (2 tools)
- `system_health` - Health checks
- `analytics_overview` - Usage analytics

### 8. Utilities (3 tools)
- `get_server_info` - Server capabilities
- `explain_capabilities` - Detailed guide
- MCP Resources for documentation

## 📊 Comparison: Original vs Enhanced

| Feature | Original | Enhanced v2.0 |
|---------|----------|---------------|
| **Tools** | 8 basic | 35 advanced |
| **Search Strategies** | 1 (vanilla) | 3 (hybrid, hyde, fusion) |
| **Knowledge Graph** | ❌ | ✅ Full support |
| **Streaming** | ❌ | ✅ RAG & Agent |
| **Metadata Management** | ❌ | ✅ Full CRUD |
| **Conversations** | Basic | ✅ Full management |
| **Monitoring** | Status only | ✅ Full analytics |
| **Error Handling** | Basic | ✅ Retry + backoff |
| **Batch Operations** | ❌ | ✅ Parallel queries |
| **Extended Thinking** | ❌ | ✅ 4096 token budget |

## 🛡️ Error Handling

### Automatic Retries
The server automatically retries failed requests with exponential backoff:

```python
# Configuration
MAX_RETRIES = 3  # Attempts: initial + 3 retries
TIMEOUT = 120.0  # 2 minutes per request

# Backoff schedule:
# Attempt 1: Immediate
# Attempt 2: Wait 1 second
# Attempt 3: Wait 2 seconds
# Attempt 4: Wait 4 seconds
```

### Error Messages
All tools provide detailed error messages with:
- Error type and description
- Suggested fixes
- Relevant documentation links

## 📖 Workflows

### Workflow 1: Basic RAG Pipeline
```python
# 1. Check system
health = await system_health()

# 2. Create collection
collection = await collection_create_smart(
    name="Research",
    description="Research documents"
)

# 3. Upload documents (use existing tools)
# ...

# 4. Search
results = await r2r_search_advanced(
    query="machine learning",
    collection_ids=[collection["collection_id"]]
)

# 5. Generate answer
answer = await r2r_rag_extended(
    query="Explain machine learning",
    collection_ids=[collection["collection_id"]]
)
```

### Workflow 2: Knowledge Graph Pipeline
```python
# 1. Upload document
# ...

# 2. Extract graph
graph = await graph_extract(
    document_id="doc_id",
    entity_types=["Person", "Organization", "Technology"]
)

# 3. Query graph
results = await graph_query(
    collection_id="coll_id",
    query="What technologies are used?"
)

# 4. Create custom entities
entity = await graph_entities_create(
    collection_id="coll_id",
    name="Custom Entity",
    entity_type="Technology"
)
```

### Workflow 3: Research Conversation
```python
# 1. Start research
response = await r2r_agent_extended(
    message="Research quantum computing",
    mode="research",
    enable_thinking=True
)

# 2. Extract conversation_id
conv_id = response["conversation_id"]

# 3. Continue conversation
for question in follow_up_questions:
    response = await r2r_agent_extended(
        message=question,
        conversation_id=conv_id,
        mode="research"
    )

# 4. View history
history = await conv_get(conv_id)

# 5. Analyze conversation
# ...
```

## 🔗 Integration Examples

### With Claude Code
```json
{
  "mcpServers": {
    "r2r-enhanced": {
      "command": "python",
      "args": ["server_enhanced.py"],
      "env": {
        "R2R_BASE_URL": "http://localhost:7272",
        "API_KEY": "your_key"
      }
    }
  }
}
```

### With Cursor
```json
{
  "mcp_servers": {
    "r2r-enhanced": {
      "command": "python",
      "args": ["server_enhanced.py"],
      "env": {
        "R2R_BASE_URL": "http://localhost:7272",
        "API_KEY": "your_key"
      }
    }
  }
}
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test specific functionality
pytest tests/test_search.py
pytest tests/test_knowledge_graph.py
pytest tests/test_conversations.py
```

## 📈 Performance Tips

1. **Use Appropriate Search Strategy**
   - Hybrid: General queries (fast, accurate)
   - HyDE: Conceptual queries (slower, more nuanced)
   - RAG-Fusion: Comprehensive (slower, most thorough)

2. **Optimize Search Limits**
   - Start with 5-10 results
   - Increase only if needed
   - Use filters to narrow results

3. **Enable Caching**
   - Results are cached for 5 minutes
   - Reduces API calls
   - Improves response time

4. **Batch Operations**
   - Use `batch_search` for multiple queries
   - Process documents in parallel
   - Reduces total execution time

## 🔐 Security

- **API Key**: Always use environment variables
- **HTTPS**: Use HTTPS in production
- **Rate Limiting**: Built-in retry with backoff
- **Validation**: Input validation on all tools
- **Error Messages**: No sensitive data in errors

## 📝 Best Practices

### Search
- Use `hybrid` for most queries
- Use `hyde` for "explain" or "what is" questions
- Use `rag_fusion` for research tasks
- Always specify `collection_ids` when possible

### RAG
- Start with 5-10 search results
- Increase `max_tokens` for complex questions
- Enable `web_search` for current information
- Use `extended` mode for comprehensive answers

### Knowledge Graph
- Extract graphs immediately after upload
- Specify entity types for better results
- Create custom entities for domain knowledge
- Query graphs for relationship discovery

### Conversations
- Use `research` mode for complex queries
- Enable `thinking` for reasoning tasks
- Reuse `conversation_id` for context
- Clean up old conversations regularly

### Monitoring
- Check `system_health()` regularly
- Monitor `collection_stats()` for insights
- Review `analytics_overview()` for usage
- Set up alerts for errors

## 🆕 Migration from v1.0

### Breaking Changes
- Tool names updated (added prefixes)
- New required parameters in some tools
- Configuration moved to environment variables

### Migration Guide
```python
# Old (v1.0)
result = await r2r_search("query", limit=3)

# New (v2.0)
result = await r2r_search_advanced(
    query="query",
    limit=3,
    strategy="hybrid"
)
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Add tests
4. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- [R2R Documentation](https://r2r-docs.sciphi.ai/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [GitHub Repository](#)

## 📞 Support

- Issues: [GitHub Issues](#)
- Discussions: [GitHub Discussions](#)
- Email: support@example.com

---

**R2R Enhanced FastMCP Server v2.0** - Production-ready RAG with advanced capabilities 🚀

