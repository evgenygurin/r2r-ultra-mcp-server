#!/usr/bin/env bash
# R2R RAG Command
# RAG query with retrieval and generation

source "$(dirname "$0")/../lib/common.sh"

# RAG-specific flags
FILTER_FIELD=""
FILTER_VALUE=""
SEARCH_STRATEGY="vanilla"
USE_GRAPH_SEARCH=false
COLLECTION_ID=""
MAX_TOKENS="$DEFAULT_MAX_TOKENS"

r2r_rag() {
    local query="$1"
    local max_tokens="${MAX_TOKENS}"

    # Build filters using jq
    local filters=$(jq -n '{}')

    if [ -n "$FILTER_FIELD" ] && [ -n "$FILTER_VALUE" ]; then
        filters=$(echo "$filters" | jq \
            --arg field "$FILTER_FIELD" \
            --arg value "$FILTER_VALUE" \
            '. + {($field): {"$eq": $value}}')
    fi

    if [ -n "$COLLECTION_ID" ]; then
        filters=$(echo "$filters" | jq \
            --arg cid "$COLLECTION_ID" \
            '. + {"collection_ids": {"$overlap": [$cid]}}')
    fi

    # Build search settings using jq
    local use_graph_json="false"
    [ "$USE_GRAPH_SEARCH" = true ] && use_graph_json="true"

    local search_settings=$(jq -n \
        --arg strategy "$SEARCH_STRATEGY" \
        --argjson use_graph "$use_graph_json" \
        --argjson filters "$filters" \
        '{
            use_hybrid_search: true,
            search_strategy: $strategy,
            filters: $filters
        } + (if $use_graph then {use_graph_search: true} else {} end)')

    # Build RAG generation config
    local rag_config=$(jq -n \
        --argjson tokens "$max_tokens" \
        '{max_tokens: $tokens}')

    # Build complete payload
    local payload=$(jq -n \
        --arg q "$query" \
        --argjson settings "$search_settings" \
        --argjson config "$rag_config" \
        '{query: $q, search_settings: $settings, rag_generation_config: $config}')

    local response=$(curl -s -X POST "${R2R_BASE_URL}/v3/retrieval/rag" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${API_KEY}" \
        -d "$payload")

    if [ "$JSON_OUTPUT" = true ]; then
        echo "$response" | jq '.'
    else
        # Extract and display the generated answer
        local answer=$(echo "$response" | jq -r '.results.generated_answer // empty')

        if [ -z "$answer" ]; then
            echo "$response" | jq '.'
        else
            echo "$answer"
        fi
    fi
}

# Show help
show_help() {
    cat << EOF
R2R RAG Command

USAGE:
    rag <query> [options]

OPTIONS:
    --max-tokens <n>            Max tokens for generation (default: $DEFAULT_MAX_TOKENS)
    --filter field=value        Filter by metadata field
    --strategy <name>           Search strategy (vanilla, hyde, rag_fusion)
    --graph                     Enable graph search (entities + relationships)
    --collection <id>           Filter by collection ID
    --json                      Output raw JSON

STRATEGIES:
    vanilla (default)           Standard semantic search (recommended)
    hyde                        Hypothetical Document Embeddings (may not work)
    rag_fusion                  Multiple queries + RRF (may not work)

EXAMPLES:
    # Basic RAG query
    rag "What is R2R?"

    # With custom token limit
    rag "Explain transformers" --max-tokens 2000

    # With filters
    rag "Python best practices" --filter document_type=pdf

    # With graph search
    rag "Knowledge graph overview" --graph

    # In specific collection
    rag "API documentation" --collection abc123

    # JSON output
    rag "RAG workflow" --json
EOF
}

# If executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    # Parse flags and positional arguments
    ARGS=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --max-tokens)
                MAX_TOKENS="$2"
                shift 2
                ;;
            --filter)
                if [[ "$2" =~ ^([^=]+)=(.+)$ ]]; then
                    FILTER_FIELD="${BASH_REMATCH[1]}"
                    FILTER_VALUE="${BASH_REMATCH[2]}"
                    shift 2
                else
                    echo "Error: --filter requires format 'field=value'" >&2
                    exit 1
                fi
                ;;
            --strategy)
                SEARCH_STRATEGY="$2"
                shift 2
                ;;
            --graph)
                USE_GRAPH_SEARCH=true
                shift
                ;;
            --collection)
                COLLECTION_ID="$2"
                shift 2
                ;;
            --json)
                JSON_OUTPUT=true
                shift
                ;;
            help|--help|-h)
                show_help
                exit 0
                ;;
            *)
                ARGS+=("$1")
                shift
                ;;
        esac
    done

    # Check if we have a query
    if [ ${#ARGS[@]} -lt 1 ]; then
        show_help
        exit 0
    fi

    r2r_rag "${ARGS[@]}"
fi
