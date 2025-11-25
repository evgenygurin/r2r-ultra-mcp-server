#!/usr/bin/env bash
# R2R Documents Management
# Create, list, delete, export documents

source "$(dirname "$0")/../lib/common.sh"

# List documents with filtering and pagination
docs_list() {
    local offset="${1:-0}"
    local limit="${2:-10}"

    print_header "Listing Documents (offset: $offset, limit: $limit)"

    curl -s -X GET "${R2R_BASE_URL}/v3/documents?offset=${offset}&limit=${limit}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq -r '.results[] |
            "ID: \(.id)\n" +
            "Title: \(.metadata.title // "Untitled")\n" +
            "Status: \(.ingestion_status)\n" +
            "Collections: \(.collection_ids | join(", "))\n" +
            "Created: \(.created_at)\n" +
            "---"'
}

# Get document details
docs_get() {
    local doc_id="$1"

    print_header "Getting Document: $doc_id"

    curl -s -X GET "${R2R_BASE_URL}/v3/documents/${doc_id}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.'
}

# Delete document
docs_delete() {
    local doc_id="$1"

    print_header "Deleting Document: $doc_id"

    curl -s -X DELETE "${R2R_BASE_URL}/v3/documents/${doc_id}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.'

    print_success "Document deleted"
}

# Upload document
docs_upload() {
    local file_path="$1"
    local collection_ids="${2:-}"
    local metadata="${3:-}"

    if [ ! -f "$file_path" ]; then
        print_error "File not found: $file_path"
        return 1
    fi

    print_header "Uploading Document: $file_path"

    local form_data="-F file=@${file_path}"

    if [ -n "$collection_ids" ]; then
        form_data="${form_data} -F collection_ids=${collection_ids}"
    fi

    if [ -n "$metadata" ]; then
        form_data="${form_data} -F metadata=${metadata}"
    fi

    curl -s -X POST "${R2R_BASE_URL}/v3/documents" \
        -H "Authorization: Bearer ${API_KEY}" \
        ${form_data} \
        | jq '.'

    print_success "Document uploaded"
}

# Export documents to CSV
docs_export() {
    local output_file="${1:-documents_export.csv}"

    print_header "Exporting Documents to $output_file"

    curl -s -X POST "${R2R_BASE_URL}/v3/documents/export" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{"include_header":true}' \
        > "$output_file"

    print_success "Documents exported to $output_file"
    head -5 "$output_file"
}

# Extract knowledge graph from document
docs_extract() {
    local doc_id="$1"
    local entity_types="${2:-Person,Organization,Technology,Concept}"

    print_header "Extracting Knowledge Graph from Document: $doc_id"
    print_info "Entity types: $entity_types"

    curl -s -X POST "${R2R_BASE_URL}/v3/documents/${doc_id}/extract" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{\"entity_types\":[\"${entity_types//,/\",\"}\"],\"relation_types\":[\"works_at\",\"developed\",\"uses\",\"part_of\",\"related_to\"]}" \
        | jq '.'

    print_success "Extraction initiated. Use docs get <id> to check status."
}

# Show help
show_help() {
    cat << EOF
R2R Documents Commands

USAGE:
    docs <action> [arguments]

ACTIONS:
    list [offset] [limit]              List documents (default: 0, 10)
    get <doc_id>                       Get document details
    delete <doc_id>                    Delete document
    upload <file> [collection_ids]     Upload document
    export [output_file]               Export documents to CSV
    extract <doc_id> [entity_types]    Extract knowledge graph

EXAMPLES:
    docs list
    docs list 10 20
    docs get abc123-def456-ghi789
    docs upload document.pdf "collection1,collection2"
    docs delete abc123-def456-ghi789
    docs export my_docs.csv
    docs extract abc123 "Person,Organization"
EOF
}

# Command dispatcher
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    ACTION="${1:-help}"
    shift || true

    case "$ACTION" in
        list) docs_list "$@" ;;
        get) docs_get "$@" ;;
        delete) docs_delete "$@" ;;
        upload) docs_upload "$@" ;;
        export) docs_export "$@" ;;
        extract) docs_extract "$@" ;;
        help|--help|-h) show_help ;;
        *) echo "Unknown action: $ACTION" >&2; show_help; exit 1 ;;
    esac
fi
