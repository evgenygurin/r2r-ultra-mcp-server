---
name: r2r-collections
description: List and manage R2R collections
allowed-tools: Bash
denied-tools: Write, Edit
---

# R2R Collections Management

Action: **$1** (list, create, add-doc, add-user, optional)

## Instructions

Use the bash script `.claude/scripts/r2r_advanced.sh` to manage collections.

### Available Commands:

**List collections:**
```bash
.claude/scripts/r2r_advanced.sh collections list
```

**Create collection:**
```bash
.claude/scripts/r2r_advanced.sh collections create "Collection Name" "Description"
```

**Add document to collection:**
```bash
.claude/scripts/r2r_advanced.sh collections add-document <collection_id> <document_id>
```

**Add user to collection:**
```bash
.claude/scripts/r2r_advanced.sh collections add-user <user_id> <collection_id>
```

Present collections in a clear format:
- **Collection ID:** UUID for commands
- **Name:** Human-readable name
- **Description:** Purpose or content type
- **Document count:** Number of documents (if available)

## Next Steps

After listing collections, suggest:
1. Search within a specific collection
2. Create a new collection
3. Add documents to collection
4. Build knowledge graph for collection

## Examples

```bash
# List all collections
/r2r-collections list

# Create new collection
/r2r-collections create "AI Research" "Papers about artificial intelligence"

# Add document to collection
/r2r-collections add-doc <collection_id> <document_id>

# Add user to collection
/r2r-collections add-user <user_id> <collection_id>
```

## Collection Features

Collections allow you to:
- Organize documents by topic/project
- Apply per-collection permissions
- Filter search results by collection
- Build collection-specific knowledge graphs
- Share access with specific users
