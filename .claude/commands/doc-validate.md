---
name: doc-validate
description: Validate documentation structure and links
allowed-tools: Bash, Grep, Glob, Read
denied-tools: Write, Edit
---

Validate documentation structure:

!echo "=== Checking file numbering ==="
!fd -e md '^[0-9]{2}-' docs/ | sort

!echo "=== Checking internal links ==="
!rg '\[.*\]\(\./[^)]+\.md\)' docs/ -o

!echo "=== README files ==="
!fd README.md docs/

Report:
1. Missing sequence numbers (gaps in 01-XX)
2. Broken internal links
3. Missing README.md files
4. Files without proper structure (no title, no sections)

Provide fix recommendations for each issue found.
