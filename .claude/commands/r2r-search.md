---
name: r2r-search
description: Search R2R knowledge base with semantic/hybrid search
allowed-tools: Bash
denied-tools: Write, Edit
---

# R2R Knowledge Base Search

Search query: **$1**

Options:
- Limit: **$2** (default: 3 results)
- Flags: **--verbose** (show full metadata), **--json** (raw JSON output)

## Instructions

Use the bash script `.claude/scripts/r2r_client.sh` to perform hybrid search (semantic + fulltext).

Execute the search command:
```bash
.claude/scripts/r2r_client.sh search "$1" ${2:-3}
```

Additional flags:
- `--verbose` - Show detailed metadata (Document ID, Chunk ID, Title, Collections, Score)
- `--json` - Output raw JSON for further processing

Present results in clear format:
1. **Score:** X.XX
2. **Document:** Title [chunk_id]
3. **Text excerpt**

If no query provided, prompt user for a search query.

## Examples

```bash
# Basic search
/r2r-search "machine learning algorithms"

# With custom limit
/r2r-search "neural networks" 10

# Verbose output with metadata
/r2r-search "transformer architecture" 5 --verbose

# JSON output for processing
/r2r-search "deep learning" --json
```
