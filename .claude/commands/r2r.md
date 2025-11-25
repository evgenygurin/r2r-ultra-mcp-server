---
name: r2r
description: Show R2R quick reference
allowed-tools: Read
denied-tools: Write, Edit, Bash
---

# R2R Quick Reference

Show R2R quick reference with bash script commands.

## Available Scripts

**`.claude/scripts/r2r_client.sh`** - Query operations:
- `search <query> [limit]` - Hybrid search (semantic + fulltext)
- `rag <query> [max_tokens]` - RAG query with generation
- `agent <query> [mode] [conv_id] [max_tokens]` - Agent conversation

**`.claude/scripts/r2r_advanced.sh`** - Management operations:
- `docs list|get|delete|export|extract` - Document management
- `collections list|create|add-document` - Collection management
- `graph entities|relationships|communities|build-communities|pull` - Knowledge graphs
- `search filtered|strategy|graph` - Advanced search
- `analytics collection|document` - Analytics

## Slash Commands

- `/r2r-search "query" [limit]` - Quick search
- `/r2r-rag "query" [max_tokens]` - RAG query
- `/r2r-agent "message" [mode]` - Agent conversation
- `/r2r-collections [action]` - Manage collections
- `/r2r-upload <file> [collection_ids]` - Upload document

## Flags

- `--json` - Raw JSON output
- `--verbose` - Detailed metadata (search)
- `--thinking` - Extended thinking (agent, 4096 token budget)

## Examples

Read `.claude/scripts/R2R_EXAMPLES.md` for comprehensive examples with real code and expected results.

Focus on:
1. Bash script commands and flags
2. Slash command usage
3. Practical examples
4. Common workflows
