# R2R FastMCP Server

FastMCP server providing tools for R2R API integration. Maps 1-to-1 with slash commands in `.claude/commands/`.

## Features

### 8 MCP Tools

1. **r2r_search** - Hybrid search (semantic + fulltext)
2. **r2r_rag** - RAG query with generation
3. **r2r_agent** - Multi-turn agent conversation
4. **r2r_collections_list/create/get** - Collection management
5. **r2r_upload** - Document upload
6. **r2r_examples** - Interactive examples catalog
7. **r2r_workflows** - Automated workflows
8. **r2r_quick** - Quick one-line tasks

## Installation

```bash
# Install dependencies with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

## Configuration

Create `.env` file in project root:

```bash
R2R_BASE_URL=http://localhost:7272  # Your R2R instance URL
API_KEY=your_api_key_here            # R2R API key
```

## Installation in Cursor

### Step 1: Install Dependencies

```bash
cd /Users/laptop/dev/r2r-fastmcp/mcp-server
uv sync
# or
pip install -e .
```

### Step 2: Configure MCP Server

Open Cursor Settings (`Cmd + ,`) → search "MCP" → click "Edit in settings.json"

Or manually edit `~/.cursor/settings.json`:

```json
{
  "mcpServers": {
    "r2r": {
      "command": "python",
      "args": ["/Users/laptop/dev/r2r-fastmcp/mcp-server/server.py"],
      "env": {
        "R2R_BASE_URL": "{{R2R_BASE_URL}}",
        "API_KEY": "{{API_KEY}}"
      }
    }
  }
}
```

### Step 3: Set Environment Variables

Create `~/.cursor/.env` or add to your shell profile:

```bash
export R2R_BASE_URL=http://localhost:7272
export API_KEY=your_api_key_here
```

### Step 4: Restart Cursor

Close and reopen Cursor to load the MCP server.

### Step 5: Verify Installation

In Cursor chat, type `@` and you should see `r2r` MCP server with available tools.

## Deployment

> **💡 Quick Start**: See [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) for 3-minute cloud deployment!

Multiple deployment options for different use cases.

### Quick Options

| Method | Difficulty | Best For | Link |
|--------|------------|----------|------|
| **FastMCP Cloud** | ⭐ Easiest | Production, zero-config | [Guide](./FASTMCP_CLOUD_DEPLOY.md) |
| **HTTP/SSE Server** | ⭐ Easy | Remote access, self-hosted | [Guide](./DEPLOYMENT.md) |
| **Docker** | ⭐⭐ Medium | Containers, cloud | [Guide](./DEPLOYMENT.md) |
| **Systemd** | ⭐⭐ Medium | Linux servers, always-on | [Guide](./DEPLOYMENT.md) |
| **Stdio (Local)** | ⭐ Easy | Cursor/Claude Desktop (local) | See above |

### 🚀 FastMCP Cloud (Recommended)

Deploy to production in **3 steps** with automatic HTTPS, monitoring, and GitHub integration:

1. Push your code to GitHub
2. Visit [fastmcp.cloud](https://fastmcp.cloud) and connect your repo
3. Configure entrypoint: `mcp-server/server.py:mcp`

**Result**: Your server at `https://your-project.fastmcp.app/mcp` ✅

**Features**:
- ✅ Free for personal use
- ✅ Automatic HTTPS & SSL
- ✅ Auto-redeploy on git push
- ✅ Built-in monitoring dashboard
- ✅ Environment variables management
- ✅ PR preview deployments

**📚 Full Guide**: [FASTMCP_CLOUD_DEPLOY.md](./FASTMCP_CLOUD_DEPLOY.md)

### Quick Start: Local HTTP/SSE Server

For self-hosted deployment:

```bash
cd /Users/laptop/dev/r2r-fastmcp/mcp-server

# Run server with HTTP/SSE transport
python server.py --transport sse --port 8000

# Or with fastmcp CLI
fastmcp run server.py --transport sse --port 8000

# Access at: http://localhost:8000/sse
```

### Connect from Cursor (Remote)

```json
{
  "mcpServers": {
    "r2r-cloud": {
      "url": "https://your-project.fastmcp.app/mcp",
      "transport": "sse"
    }
  }
}
```

Or for self-hosted:

```json
{
  "mcpServers": {
    "r2r-remote": {
      "url": "http://your-server:8000/sse",
      "transport": "sse"
    }
  }
}
```

### Full Deployment Guides

**☁️ [FASTMCP_CLOUD_DEPLOY.md](./FASTMCP_CLOUD_DEPLOY.md)** - Zero-config cloud deployment:
- Step-by-step setup with GitHub
- Environment variables configuration
- Automatic redeploy workflows
- Monitoring and metrics
- PR preview deployments
- FAQ and troubleshooting

**🔧 [DEPLOYMENT.md](./DEPLOYMENT.md)** - Self-hosted deployment:
- Docker & Docker Compose
- Systemd service configuration
- Nginx reverse proxy with SSL
- Environment variables best practices
- Monitoring and logging
- Security hardening
- Update strategies
- Troubleshooting guide

## Usage

### Run MCP Server (Standalone)

```bash
# Stdio transport
python server.py

# Or with fastmcp CLI
fastmcp run server.py
```

### Configure in Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "r2r": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-server/server.py"],
      "env": {
        "R2R_BASE_URL": "http://localhost:7272",
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Tool Examples

### Search

```python
# Basic search
result = await r2r_search("machine learning", limit=3)

# Collection-specific search
result = await r2r_search(
    "neural networks",
    limit=5,
    collection_id="col_abc123"
)
```

### RAG Query

```python
# Simple question
answer = await r2r_rag("What is FastMCP?", max_tokens=1000)

# Detailed analysis
answer = await r2r_rag(
    "Explain transformer architecture in detail",
    max_tokens=8000
)
```

### Agent Conversation

```python
# Initial query
response = await r2r_agent(
    "Research AI safety implications",
    mode="research"
)

# Follow-up
response = await r2r_agent(
    "Tell me more about alignment",
    conversation_id=response["conversation_id"]
)

# With extended thinking
response = await r2r_agent(
    "Deep analysis required",
    mode="research",
    enable_thinking=True
)
```

### Collections

```python
# List collections
collections = await r2r_collections_list(limit=10)

# Create collection
collection = await r2r_collections_create(
    "AI Research",
    "Papers about artificial intelligence"
)

# Get collection details
details = await r2r_collections_get("col_abc123")
```

### Quick Tasks

```python
# Quick search + RAG answer
result = await r2r_quick("ask", query="What is RAG?")

# System status
status = await r2r_quick("status")

# Quick collection create
col = await r2r_quick("col", name="Test", description="Test collection")
```

### Workflows

```python
# Research workflow with extended thinking
result = await r2r_workflows(
    "research",
    query="Analyze quantum computing implications"
)

# Create collection workflow
result = await r2r_workflows(
    "create-collection",
    name="Research Papers",
    description="Academic papers"
)
```

## Mapping to Slash Commands

| MCP Tool | Slash Command | Bash Script |
|----------|---------------|-------------|
| `r2r_search` | `/r2r-search` | `.claude/scripts/r2r search` |
| `r2r_rag` | `/r2r-rag` | `.claude/scripts/r2r rag` |
| `r2r_agent` | `/r2r-agent` | `.claude/scripts/r2r agent` |
| `r2r_collections_*` | `/r2r-collections` | `.claude/scripts/r2r collections` |
| `r2r_upload` | `/r2r-upload` | `.claude/scripts/r2r docs upload` |
| `r2r_examples` | `/r2r-examples` | `.claude/scripts/examples.sh` |
| `r2r_workflows` | `/r2r-workflows` | `.claude/scripts/workflows.sh` |
| `r2r_quick` | `/r2r-quick` | `.claude/scripts/quick.sh` |

## API Endpoints Used

- **Search:** `POST /v3/retrieval/search`
- **RAG:** `POST /v3/retrieval/rag`
- **Agent:** `POST /v3/retrieval/agent`
- **Collections List:** `GET /v3/collections`
- **Collections Create:** `POST /v3/collections`
- **Collections Get:** `GET /v3/collections/{id}`
- **Documents Create:** `POST /v3/documents/create`

## Development

### Run Tests

```bash
pytest
```

### Lint & Format

```bash
ruff check .
ruff format .
```

## Architecture

```text
┌─────────────────┐
│  Claude Code    │  Uses MCP tools
│   (Client)      │  via MCP protocol
└────────┬────────┘
         │ MCP stdio
┌────────▼────────┐
│  FastMCP Server │  8 @mcp.tool decorators
│  (server.py)    │  Map to R2R API
└────────┬────────┘
         │ HTTP + JSON
┌────────▼────────┐
│      R2R        │  v3 API endpoints
│   (Backend)     │  /v3/retrieval/*
└─────────────────┘
```

## Comparison: Bash vs MCP

### Before (Bash Scripts)

```bash
# Requires shell execution
.claude/scripts/r2r search "query" --limit 3

# Output: text parsing needed
```

### After (MCP Tools)

```python
# Native function call
result = await r2r_search("query", limit=3)

# Output: structured JSON
```

### Benefits of MCP

1. **Type Safety:** Python type hints, JSON schemas
2. **Error Handling:** Proper exceptions, validation
3. **Integration:** Native tool calling in Claude
4. **Async Support:** Non-blocking I/O
5. **Composability:** Tools can call other tools
6. **Testing:** Unit tests for each tool
7. **Documentation:** Auto-generated from docstrings

## License

MIT
