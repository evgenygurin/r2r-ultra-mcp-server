---
name: r2r
description: Show R2R quick reference
allowed-tools: Read
denied-tools: Write, Edit, Bash
---

# R2R Quick Reference

Show R2R quick reference with modular CLI commands.

## Modular R2R CLI

**`.claude/scripts/r2r`** - Unified command interface (8 commands, 48 sub-commands)

### Core Commands (3):
- `search <query> [--limit N]` - Hybrid search (semantic + fulltext)
- `rag <query> [--max-tokens N]` - RAG query with generation
- `agent <query> [--mode research|rag]` - Multi-turn agent

### Management Commands (5):
- `docs` - Document management (14 sub-commands: list, get, upload, delete, extract, etc.)
- `collections` - Collection management (6 sub-commands: list, create, add-doc, remove-doc, etc.)
- `conversation` - Conversation management (5 sub-commands: list, create, get, add-message, delete)
- `graph` - Knowledge graph operations (20 sub-commands: entities, relationships, communities, etc.)
- `analytics` - System analytics (3 sub-commands: system, collection, document)

## Slash Commands

- `/r2r-search "query" [limit]` - Quick search
- `/r2r-rag "query" [max_tokens]` - RAG query
- `/r2r-agent "message" [mode]` - Agent conversation
- `/r2r-collections [action]` - Manage collections
- `/r2r-upload <file> [collection_ids]` - Upload document

## Common Flags (GNU-style)

**Output modes:**
- `--quiet, -q` - Minimal output (one line per result)
- `--json` - Raw JSON output
- `--verbose, -v` - Full details with metadata

**Search/RAG options:**
- `--limit, -l <n>` - Number of results (default: 3)
- `--max-tokens, -t <n>` - Max tokens for generation (default: 4000)
- `--graph, -g` - Enable graph search
- `--collection, -c <id>` - Filter by collection
- `--filter, -f <key=val>` - Custom filters

**Agent options:**
- `--mode, -m <mode>` - research (default) or rag
- `--conversation, -c <id>` - Continue conversation
- `--thinking` - Extended thinking (4096 token budget)
- `--show-tools` - Show tool calls
- `--show-sources` - Show citations

## Quick Examples

```bash
# Core commands
r2r search "transformers" --limit 5 -q
r2r rag "What is RAG?" --show-sources
r2r agent "Explain DeepSeek" --thinking

# Management
r2r docs list -l 10 -q
r2r collections create -n "Research Papers"
r2r graph entities <collection_id> -l 50

# Advanced
r2r search "AI" --graph --collection abc123
r2r rag "Question" --filter category=research --max-tokens 8000
r2r agent "Continue discussion" -c <conv_id> --show-tools
```

## Documentation

- **Full reference:** `.claude/scripts/README.md`
- **CLI help:** `r2r <command> help`
- **All commands:** `r2r search help`, `r2r rag help`, `r2r agent help`, etc.
