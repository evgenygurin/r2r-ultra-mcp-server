"""
Unit tests for R2R Ultra MCP Server.
"""


def test_server_initialization(mcp_server):
    """Test that server initializes correctly."""
    assert mcp_server is not None
    assert mcp_server.name == "R2R Ultra MCP Server v3.0"


def test_server_has_tools(mcp_server):
    """Test that server has registered tools."""
    tools = mcp_server._list_tools()
    assert len(tools) > 0

    tool_names = [tool.name for tool in tools]

    # Check for expected tools
    assert "get_server_capabilities" in tool_names
    assert "r2r_search_with_progress" in tool_names
    assert "r2r_rag_with_sampling" in tool_names
    assert "batch_document_analysis" in tool_names
    assert "smart_collection_search" in tool_names
    assert "get_performance_stats" in tool_names
    assert "clear_cache" in tool_names


def test_server_has_resources(mcp_server):
    """Test that server has registered resources."""
    resources = mcp_server._list_resources()
    assert len(resources) > 0

    resource_uris = [r.uri for r in resources]

    # Check for expected resources
    assert "r2r://server/stats" in resource_uris
    assert "r2r://config" in resource_uris


def test_server_has_prompts(mcp_server):
    """Test that server has registered prompts."""
    prompts = mcp_server._list_prompts()
    assert len(prompts) > 0

    prompt_names = [p.name for p in prompts]

    # Check for expected prompts
    assert "research_question_prompt" in prompt_names
    assert "code_review_prompt" in prompt_names
    assert "data_analysis_prompt" in prompt_names


def test_server_has_middleware(mcp_server):
    """Test that server has middleware configured."""
    assert hasattr(mcp_server, '_middleware')
    middleware = mcp_server._middleware
    assert len(middleware) == 5  # 5 middleware components

    middleware_classes = [m.__class__.__name__ for m in middleware]

    # Check for expected middleware
    assert "LoggingMiddleware" in middleware_classes
    assert "TimingMiddleware" in middleware_classes
    assert "RateLimitingMiddleware" in middleware_classes
    assert "ErrorHandlingMiddleware" in middleware_classes
    assert "CachingMiddleware" in middleware_classes
