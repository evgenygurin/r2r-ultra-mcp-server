#!/usr/bin/env bash
# R2R Analytics Commands
# Collection and document statistics

source "$(dirname "$0")/../lib/common.sh"

# Get collection statistics
analytics_collection() {
    local collection_id="$1"

    print_header "Collection Analytics: $collection_id"

    echo -e "\n${YELLOW}Collection Info:${NC}"
    curl -s -X GET "${R2R_BASE_URL}/v3/collections/${collection_id}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '{
            name,
            document_count,
            user_count,
            graph_cluster_status,
            graph_sync_status,
            created_at,
            updated_at
        }'

    echo -e "\n${YELLOW}Entities Count:${NC}"
    curl -s -X GET "${R2R_BASE_URL}/v3/graphs/${collection_id}/entities?limit=1" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.total_entries'

    echo -e "\n${YELLOW}Relationships Count:${NC}"
    curl -s -X GET "${R2R_BASE_URL}/v3/graphs/${collection_id}/relationships?limit=1" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.total_entries'

    echo -e "\n${YELLOW}Communities Count:${NC}"
    curl -s -X GET "${R2R_BASE_URL}/v3/graphs/${collection_id}/communities?limit=1" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.total_entries'
}

# Document insights
analytics_document() {
    local doc_id="$1"

    print_header "Document Analytics: $doc_id"

    curl -s -X GET "${R2R_BASE_URL}/v3/documents/${doc_id}" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '{
            id,
            title: .metadata.title,
            ingestion_status,
            collection_ids,
            created_at,
            updated_at,
            metadata
        }'
}

# System statistics
analytics_system() {
    print_header "System Analytics"

    echo -e "\n${YELLOW}Total Documents:${NC}"
    curl -s -X GET "${R2R_BASE_URL}/v3/documents?limit=1" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.total_entries'

    echo -e "\n${YELLOW}Total Collections:${NC}"
    curl -s -X GET "${R2R_BASE_URL}/v3/collections?limit=1" \
        -H "Authorization: Bearer ${API_KEY}" \
        | jq '.total_entries'
}

# Show help
show_help() {
    cat << EOF
R2R Analytics Commands

USAGE:
    analytics <action> [arguments]

ACTIONS:
    collection <collection_id>     Collection statistics and graph metrics
    document <document_id>         Document details and metadata
    system                         System-wide statistics

EXAMPLES:
    analytics collection abc123-def456
    analytics document doc789-ghi012
    analytics system
EOF
}

# Command dispatcher
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    ACTION="${1:-help}"
    shift || true

    case "$ACTION" in
        collection|coll) analytics_collection "$@" ;;
        document|doc) analytics_document "$@" ;;
        system|sys) analytics_system "$@" ;;
        help|--help|-h) show_help ;;
        *) echo "Unknown action: $ACTION" >&2; show_help; exit 1 ;;
    esac
fi
