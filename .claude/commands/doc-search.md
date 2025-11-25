---
name: doc-search
description: Search documentation by keyword or topic
allowed-tools: Read, Grep, Glob
denied-tools: Write, Edit, Bash
---

Search the documentation for: $1

Use these commands to find relevant content:
!rg -i "$1" docs/ --type md -l | head -20

For each found file, provide:
1. File path and section title
2. Relevant excerpt (2-3 sentences)
3. Link format: `[Title](./path/to/file.md)`

Group results by technology (R2R, FastMCP, Claude Code).
