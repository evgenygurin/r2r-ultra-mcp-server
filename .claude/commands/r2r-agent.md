---
name: r2r-agent
description: Multi-turn conversation with R2R agent
allowed-tools: Bash
denied-tools: Write, Edit
---

# R2R Agent Conversation

Message: **$1**

Options:
- Mode: **$2** (rag/research, default: **research**)
  - `rag`: Standard RAG with knowledge base tools
  - `research`: Advanced mode with reasoning, critique, code execution
- Conversation ID: **$3** (optional, for multi-turn follow-ups)
- Max tokens: **$4** (default: 8000)
- Flags: **--thinking** (enable extended thinking with 4096 token budget), **--json** (raw JSON output)

## Instructions

Use the bash script `.claude/scripts/r2r_client.sh` to interact with R2R agent.

Execute the agent command:
```bash
.claude/scripts/r2r_client.sh agent "$1" ${2:-research} ${3:-""} ${4:-8000}
```

**First message:** The agent creates a new conversation and returns conversation_id to stderr.
**Follow-ups:** Use the conversation_id from previous response to continue.

### Modes:

**RAG Mode:**
- Best for: Direct questions, fact retrieval
- Tools: `search_file_knowledge`, `search_file_descriptions`, `get_file_content`, `web_search`, `web_scrape`

**Research Mode (DEFAULT):**
- Best for: Complex analysis, multi-step reasoning, deep exploration
- Tools: `rag`, `reasoning`, `critique`, `python_executor`
- Features: Advanced reasoning capabilities

### Extended Thinking:

Add `--thinking` flag for complex queries:
- Enables 4096 token reasoning budget
- Best for: philosophical questions, deep analysis, multi-step reasoning

Present the agent response with:
- **Response:** Agent's answer (clean text)
- **Conversation ID:** For follow-ups (from stderr)
- **Mode:** Current mode
- **Thinking:** If extended thinking used

If no message provided, prompt user for a message.

## Examples

```bash
# Basic research query (default mode)
/r2r-agent "What is DeepSeek R1?"

# RAG mode for simple question
/r2r-agent "What are FastMCP decorators?" rag

# Continue conversation (capture conv_id from previous response)
/r2r-agent "Tell me more details" research <conversation_id>

# Extended thinking for deep analysis
/r2r-agent "Analyze philosophical implications of RAG systems" research "" "" --thinking

# Multi-turn with thinking
/r2r-agent "Deep question" research <conversation_id> "" --thinking

# JSON output
/r2r-agent "Query" research "" "" --json
```

## Multi-turn Tips

- Research mode is default for better reasoning
- Extended thinking adds deep analytical capabilities
- Save conversation_id from stderr for follow-ups
- Conversations maintain context across turns
- Use RAG mode only for simple factual queries
