---
name: doc-stats
description: Show documentation statistics
allowed-tools: Bash, Glob
denied-tools: Write, Edit
---

Generate documentation statistics:

!echo "=== Files by directory ==="
!fd -e md . docs/r2r | wc -l | xargs echo "R2R:"
!fd -e md . docs/fastmcp | wc -l | xargs echo "FastMCP:"
!fd -e md . docs/claude_code | wc -l | xargs echo "Claude Code:"

!echo "=== Code examples ==="
!rg -c '```' docs/r2r/*.md 2>/dev/null | awk -F: '{sum+=$2} END {print "R2R:", sum}'
!rg -c '```' docs/fastmcp/*.md 2>/dev/null | awk -F: '{sum+=$2} END {print "FastMCP:", sum}'
!rg -c '```' docs/claude_code/*.md 2>/dev/null | awk -F: '{sum+=$2} END {print "Claude Code:", sum}'

!echo "=== Total lines ==="
!wc -l docs/**/*.md | tail -1

Format as a summary table.
