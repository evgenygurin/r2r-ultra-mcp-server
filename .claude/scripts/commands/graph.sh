#!/usr/bin/env bash
# R2R Knowledge Graph Commands
# Manage entities, relationships, and communities

source "$(dirname "$0")/../lib/common.sh"

# List entities in collection
graph_entities() {
    local collection_id="$1"
    local limit="${2:-20}"

    print_header "Listing Entities in Collection: $collection_id"

    curl -s -X GET "${R2R_BASE_URL}/v3/graphs/${collection_id}/entities?limit=${limit}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq -r '.results[] |
            "Name: \(.name)\n" +
            "Category: \(.category)\n" +
            "Description: \(.description)\n" +
            "---"'
}

# List relationships in collection
graph_relationships() {
    local collection_id="$1"
    local limit="${2:-20}"

    print_header "Listing Relationships in Collection: $collection_id"

    curl -s -X GET "${R2R_BASE_URL}/v3/graphs/${collection_id}/relationships?limit=${limit}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq -r '.results[] |
            "\(.subject) -> \(.predicate) -> \(.object)\n" +
            "Description: \(.description)\n" +
            "Weight: \(.weight // "N/A")\n" +
            "---"'
}

# List communities in collection
graph_communities() {
    local collection_id="$1"

    print_header "Listing Communities in Collection: $collection_id"

    curl -s -X GET "${R2R_BASE_URL}/v3/graphs/${collection_id}/communities" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq -r '.results[] |
            "ID: \(.id)\n" +
            "Name: \(.name)\n" +
            "Summary: \(.summary)\n" +
            "Rating: \(.rating // "N/A")/10\n" +
            "Findings:\n\(.findings | join("\n- "))\n" +
            "---"'
}

# Build communities for collection
graph_build_communities() {
    local collection_id="$1"

    print_header "Building Communities for Collection: $collection_id"

    curl -s -X POST "${R2R_BASE_URL}/v3/graphs/${collection_id}/communities/build" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{"message":"Building communities"}' \
        | jq '.'

    print_success "Community building initiated"
}

# Pull graph data (sync)
graph_pull() {
    local collection_id="$1"

    print_header "Syncing Graph Data for Collection: $collection_id"

    curl -s -X POST "${R2R_BASE_URL}/v3/graphs/${collection_id}/pull" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.'

    print_success "Graph data synchronized"
}

# Create entity
graph_create_entity() {
    local collection_id="$1"
    local name="$2"
    local description="$3"
    local category="${4:-Concept}"

    print_header "Creating Entity: $name"

    curl -s -X POST "${R2R_BASE_URL}/v3/graphs/${collection_id}/entities" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"${name}\",\"description\":\"${description}\",\"category\":\"${category}\"}" \
        | jq '.'

    print_success "Entity created"
}

# Create relationship
graph_create_relationship() {
    local collection_id="$1"
    local subject="$2"
    local predicate="$3"
    local object="$4"
    local description="${5:-}"

    print_header "Creating Relationship"
    print_info "$subject -> $predicate -> $object"

    curl -s -X POST "${R2R_BASE_URL}/v3/graphs/${collection_id}/relationships" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{\"subject\":\"${subject}\",\"predicate\":\"${predicate}\",\"object\":\"${object}\",\"description\":\"${description}\"}" \
        | jq '.'

    print_success "Relationship created"
}

# Show help
show_help() {
    cat << EOF
R2R Knowledge Graph Commands

USAGE:
    graph <action> [arguments]

ACTIONS:
    entities <collection_id> [limit]                List entities (default: 20)
    relationships <collection_id> [limit]           List relationships (default: 20)
    communities <collection_id>                     List communities
    build-communities <collection_id>               Build communities
    pull <collection_id>                            Sync graph data
    create-entity <col_id> <name> <desc> [cat]      Create entity
    create-rel <col_id> <subj> <pred> <obj> [desc]  Create relationship

EXAMPLES:
    graph entities abc123 30
    graph relationships abc123 50
    graph communities abc123
    graph build-communities abc123
    graph pull abc123
    graph create-entity abc123 "Claude" "AI assistant" "Technology"
    graph create-rel abc123 "Claude" "developed_by" "Anthropic" "AI company"
EOF
}

# Command dispatcher
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    ACTION="${1:-help}"
    shift || true

    case "$ACTION" in
        entities) graph_entities "$@" ;;
        relationships|rels) graph_relationships "$@" ;;
        communities) graph_communities "$@" ;;
        build-communities|build) graph_build_communities "$@" ;;
        pull|sync) graph_pull "$@" ;;
        create-entity|add-entity) graph_create_entity "$@" ;;
        create-rel|create-relationship|add-rel) graph_create_relationship "$@" ;;
        help|--help|-h) show_help ;;
        *) echo "Unknown action: $ACTION" >&2; show_help; exit 1 ;;
    esac
fi
