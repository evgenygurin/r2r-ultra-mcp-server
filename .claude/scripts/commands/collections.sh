#!/usr/bin/env bash
# R2R Collections Management
# Create, list, delete collections and manage document membership

source "$(dirname "$0")/../lib/common.sh"

# List collections
collections_list() {
    local limit="${1:-10}"
    local offset="${2:-0}"

    print_header "Listing Collections"

    curl -s -X GET "${R2R_BASE_URL}/v3/collections?limit=${limit}&offset=${offset}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq -r '.results[] |
            "ID: \(.id)\n" +
            "Name: \(.name)\n" +
            "Description: \(.description // "No description")\n" +
            "Documents: \(.document_count)\n" +
            "Users: \(.user_count)\n" +
            "Graph Status: \(.graph_cluster_status)\n" +
            "---"'
}

# Get collection details
collections_get() {
    local collection_id="$1"

    print_header "Getting Collection: $collection_id"

    curl -s -X GET "${R2R_BASE_URL}/v3/collections/${collection_id}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.'
}

# Create collection
collections_create() {
    local name="$1"
    local description="${2:-}"

    print_header "Creating Collection: $name"

    curl -s -X POST "${R2R_BASE_URL}/v3/collections" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"${name}\",\"description\":\"${description}\"}" \
        | jq '.'

    print_success "Collection created"
}

# Delete collection
collections_delete() {
    local collection_id="$1"

    print_header "Deleting Collection: $collection_id"

    curl -s -X DELETE "${R2R_BASE_URL}/v3/collections/${collection_id}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.'

    print_success "Collection deleted"
}

# Add document to collection
collections_add_document() {
    local collection_id="$1"
    local document_id="$2"

    print_header "Adding Document to Collection"
    print_info "Collection: $collection_id"
    print_info "Document: $document_id"

    curl -s -X POST "${R2R_BASE_URL}/v3/collections/${collection_id}/documents" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{\"document_id\":\"${document_id}\"}" \
        | jq '.'

    print_success "Document added to collection"
}

# Remove document from collection
collections_remove_document() {
    local collection_id="$1"
    local document_id="$2"

    print_header "Removing Document from Collection"
    print_info "Collection: $collection_id"
    print_info "Document: $document_id"

    curl -s -X DELETE "${R2R_BASE_URL}/v3/collections/${collection_id}/documents/${document_id}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.'

    print_success "Document removed from collection"
}

# Show help
show_help() {
    cat << EOF
R2R Collections Commands

USAGE:
    collections <action> [arguments]

ACTIONS:
    list [limit] [offset]                       List collections (default: 10, 0)
    get <collection_id>                         Get collection details
    create <name> [description]                 Create collection
    delete <collection_id>                      Delete collection
    add-doc <collection_id> <document_id>       Add document to collection
    remove-doc <collection_id> <document_id>    Remove document from collection

EXAMPLES:
    collections list
    collections list 20 10
    collections get abc123-def456
    collections create "My Collection" "Description here"
    collections delete abc123-def456
    collections add-doc collection123 doc456
    collections remove-doc collection123 doc456
EOF
}

# Command dispatcher
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    ACTION="${1:-help}"
    shift || true

    case "$ACTION" in
        list) collections_list "$@" ;;
        get) collections_get "$@" ;;
        create) collections_create "$@" ;;
        delete) collections_delete "$@" ;;
        add-doc|add-document) collections_add_document "$@" ;;
        remove-doc|remove-document) collections_remove_document "$@" ;;
        help|--help|-h) show_help ;;
        *) echo "Unknown action: $ACTION" >&2; show_help; exit 1 ;;
    esac
fi
