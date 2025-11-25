---
name: doc-add
description: Add new documentation section
allowed-tools: Read, Write, Glob, Bash
---

Add a new documentation section to: $1 (r2r, fastmcp, or claude_code)
Topic: $2

Steps:
1. Find next available number:
!fd -e md '^[0-9]{2}-' docs/$1/ | sort | tail -1

2. Create new file with structure:
- Title with emoji
- Introduction (2-3 sentences)
- Main content sections
- Code examples
- Best Practices
- Next Steps

3. Update docs/$1/README.md with link to new section

File naming: `{NN}-{topic-in-kebab-case}.md`
Language: Russian (text) + English (code, terms)
