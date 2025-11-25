#!/usr/bin/env bash
# R2R Agent Command
# Multi-turn agent with research/rag modes and extended thinking

source "$(dirname "$0")/../lib/common.sh"

# Agent-specific flags
AGENT_MODE="$DEFAULT_MODE"
CONVERSATION_ID=""
MAX_TOKENS="$DEFAULT_MAX_TOKENS"
EXTENDED_THINKING=false

r2r_agent() {
    local query="$1"
    local mode="$AGENT_MODE"
    local max_tokens="$MAX_TOKENS"

    # Build message object
    local message=$(jq -n \
        --arg content "$query" \
        '{role: "user", content: $content}')

    # Build RAG generation config with optional extended thinking
    local rag_config=$(jq -n \
        --argjson tokens "$max_tokens" \
        '{max_tokens: $tokens}')

    if [ "$EXTENDED_THINKING" = true ]; then
        rag_config=$(echo "$rag_config" | jq \
            '. + {extended_thinking: true, thinking_budget: 4096, temperature: 1}')
    fi

    # Build search settings
    local search_settings=$(jq -n \
        '{use_hybrid_search: true}')

    # Select tools based on mode
    local tools_array="[]"
    if [ "$mode" = "rag" ]; then
        tools_array='["search_file_knowledge","search_file_descriptions","get_file_content","web_search","web_scrape"]'
    elif [ "$mode" = "research" ]; then
        tools_array='["rag","reasoning","critique","python_executor"]'
    fi

    # Build complete payload
    local payload=$(jq -n \
        --argjson msg "$message" \
        --arg mode "$mode" \
        --argjson search_settings "$search_settings" \
        --argjson rag_config "$rag_config" \
        --argjson tools "$tools_array" \
        '{
            message: $msg,
            mode: $mode,
            search_mode: "advanced",
            search_settings: $search_settings,
            rag_generation_config: $rag_config
        } + (if $mode == "rag" then {rag_tools: $tools} elif $mode == "research" then {research_tools: $tools} else {} end)')

    # Add conversation_id if provided
    if [ -n "$CONVERSATION_ID" ]; then
        payload=$(echo "$payload" | jq \
            --arg cid "$CONVERSATION_ID" \
            '. + {conversation_id: $cid}')
    fi

    local response=$(curl -s -X POST "${R2R_BASE_URL}/v3/retrieval/agent" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${API_KEY}" \
        -d "$payload")

    if [ "$JSON_OUTPUT" = true ]; then
        echo "$response" | jq '.'
    else
        # Extract conversation_id for follow-up
        local new_conv_id=$(echo "$response" | jq -r '.results.conversation_id // empty')
        if [ -n "$new_conv_id" ] && [ -z "$CONVERSATION_ID" ]; then
            print_info "Conversation ID: $new_conv_id"
            echo ""
        fi

        # Extract and display the agent's response
        local agent_response=$(echo "$response" | jq -r '.results.messages[-1].content // empty')

        if [ -z "$agent_response" ]; then
            echo "$response" | jq '.'
        else
            echo "$agent_response"
        fi
    fi
}

# Show help
show_help() {
    cat << EOF
R2R Agent Command

USAGE:
    agent <query> [options]

OPTIONS:
    --mode <name>               Agent mode: research or rag (default: $DEFAULT_MODE)
    --conversation <id>         Continue existing conversation
    --max-tokens <n>            Max tokens for generation (default: $DEFAULT_MAX_TOKENS)
    --thinking                  Enable extended thinking (research mode)
    --json                      Output raw JSON

MODES:
    research (default)          Multi-step reasoning with tools: rag, reasoning, critique, python_executor
    rag                         Document-focused with tools: search, get_content, web_search

EXTENDED THINKING:
    --thinking flag enables deep reasoning with:
    - thinking_budget: 4096 tokens
    - temperature: 1 (creative exploration)
    - Step-by-step thought process

MULTI-TURN CONVERSATIONS:
    The agent returns a conversation_id on first query.
    Use --conversation <id> to continue the conversation.

EXAMPLES:
    # Basic agent query (research mode)
    agent "What is R2R?"

    # RAG mode for document queries
    agent "Explain hybrid search" --mode rag

    # Research mode with extended thinking
    agent "Analyze R2R architecture" --mode research --thinking

    # Continue conversation
    agent "What about FastMCP?" --conversation abc123-def456

    # Custom token limit
    agent "Comprehensive guide" --max-tokens 8000

    # JSON output
    agent "test" --json
EOF
}

# If executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    # Parse flags and positional arguments
    ARGS=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --mode)
                AGENT_MODE="$2"
                shift 2
                ;;
            --conversation)
                CONVERSATION_ID="$2"
                shift 2
                ;;
            --max-tokens)
                MAX_TOKENS="$2"
                shift 2
                ;;
            --thinking)
                EXTENDED_THINKING=true
                shift
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

    r2r_agent "${ARGS[@]}"
fi
