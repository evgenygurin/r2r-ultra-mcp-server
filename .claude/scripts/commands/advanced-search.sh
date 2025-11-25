#!/usr/bin/env bash
# R2R Advanced Search Commands
# Filtered search, strategy-based search, graph search

source "$(dirname "$0")/../lib/common.sh"

# Search with filters
search_filtered() {
    local query="$1"
    local filter_field="${2:-}"
    local filter_value="${3:-}"
    local limit="${4:-5}"

    print_header "Filtered Search: $query"

    local filter_json="{}"
    if [ -n "$filter_field" ] && [ -n "$filter_value" ]; then
        filter_json="{\"${filter_field}\":{\"\$eq\":\"${filter_value}\"}}"
        print_info "Filter: $filter_field = $filter_value"
    fi

    curl -s -X POST "${R2R_BASE_URL}/v3/retrieval/search" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${API_KEY}" \
        -d "{\"query\":\"${query}\",\"limit\":${limit},\"search_settings\":{\"use_hybrid_search\":true,\"filters\":${filter_json}}}" \
        | jq -r '.results.chunk_search_results[] |
            "Score: \(.score | tonumber | . * 100 | round / 100)\n" +
            "Doc: \(.metadata.title // "Unknown") [\(.document_id[:8])]\n" +
            "\(.text[:300])...\n" +
            "---"'
}

# Search with strategy
search_strategy() {
    local query="$1"
    local strategy="${2:-vanilla}"
    local limit="${3:-5}"

    print_header "Search with Strategy: $strategy"
    print_info "Query: $query"

    curl -s -X POST "${R2R_BASE_URL}/v3/retrieval/search" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${API_KEY}" \
        -d "{\"query\":\"${query}\",\"limit\":${limit},\"search_settings\":{\"use_hybrid_search\":true,\"search_strategy\":\"${strategy}\"}}" \
        | jq -r '.results.chunk_search_results[] |
            "Score: \(.score | tonumber | . * 100 | round / 100)\n" +
            "Text: \(.text[:200])...\n" +
            "---"'
}

# Graph search (entities + relationships)
search_graph() {
    local query="$1"
    local collection_id="${2:-}"
    local limit="${3:-5}"

    print_header "Graph Search: $query"

    local filter_json="{}"
    if [ -n "$collection_id" ]; then
        filter_json="{\"collection_ids\":{\"\$overlap\":[\"${collection_id}\"]}}"
        print_info "Collection: $collection_id"
    fi

    curl -s -X POST "${R2R_BASE_URL}/v3/retrieval/search" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${API_KEY}" \
        -d "{\"query\":\"${query}\",\"limit\":${limit},\"search_settings\":{\"use_hybrid_search\":true,\"use_graph_search\":true,\"filters\":${filter_json}}}" \
        | jq '.'
}

# Show help
show_help() {
    cat << EOF
R2R Advanced Search Commands

USAGE:
    advanced-search <action> [arguments]

ACTIONS:
    filtered <query> [field] [value] [limit]    Search with metadata filters
    strategy <query> [strategy] [limit]         Search with specific strategy
    graph <query> [collection_id] [limit]       Search using knowledge graph

STRATEGIES:
    vanilla         Standard semantic search (default, recommended)
    hyde            Hypothetical Document Embeddings (may not work)
    rag_fusion      Multiple queries + RRF (may not work)

EXAMPLES:
    advanced-search filtered "machine learning" "document_type" "pdf" 10
    advanced-search strategy "neural networks" vanilla 5
    advanced-search graph "AI research" abc123-def456 10
EOF
}

# Command dispatcher
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    ACTION="${1:-help}"
    shift || true

    case "$ACTION" in
        filtered|filter) search_filtered "$@" ;;
        strategy|strat) search_strategy "$@" ;;
        graph|kg) search_graph "$@" ;;
        help|--help|-h) show_help ;;
        *) echo "Unknown action: $ACTION" >&2; show_help; exit 1 ;;
    esac
fi
