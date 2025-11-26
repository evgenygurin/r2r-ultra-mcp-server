"""
Unit tests for middleware components.
"""
from server import (
    CachingMiddleware,
    ErrorHandlingMiddleware,
    LoggingMiddleware,
    RateLimitingMiddleware,
    TimingMiddleware,
)


def test_logging_middleware_initialization():
    """Test LoggingMiddleware initializes correctly."""
    middleware = LoggingMiddleware()
    assert middleware.request_count == 0
    assert middleware.logger is not None


def test_timing_middleware_initialization():
    """Test TimingMiddleware initializes correctly."""
    middleware = TimingMiddleware()
    assert len(middleware.operation_times) == 0
    assert middleware.logger is not None


def test_rate_limiting_middleware_initialization():
    """Test RateLimitingMiddleware initializes correctly."""
    max_requests = 100
    middleware = RateLimitingMiddleware(max_requests_per_minute=max_requests)
    assert middleware.max_requests_per_minute == max_requests
    assert len(middleware.client_requests) == 0


def test_error_handling_middleware_initialization():
    """Test ErrorHandlingMiddleware initializes correctly."""
    max_retries = 3
    middleware = ErrorHandlingMiddleware(max_retries=max_retries)
    assert middleware.max_retries == max_retries
    assert len(middleware.error_counts) == 0


def test_caching_middleware_initialization():
    """Test CachingMiddleware initializes correctly."""
    ttl = 600
    middleware = CachingMiddleware(ttl=ttl)
    assert middleware.ttl == ttl
    assert len(middleware.cache) == 0
    assert middleware.hits == 0
    assert middleware.misses == 0


def test_caching_middleware_cache_key_generation():
    """Test cache key generation."""
    from unittest.mock import Mock

    middleware = CachingMiddleware()

    # Mock context
    mock_context = Mock()
    mock_context.request = Mock()
    mock_context.request.params = {
        "name": "test_tool",
        "arguments": {"query": "test"}
    }

    cache_key = middleware._get_cache_key(mock_context)
    assert "test_tool" in cache_key
    assert "query" in cache_key


def test_middleware_count(mcp_server):
    """Test that all middleware are registered."""
    middleware_list = mcp_server._middleware

    # Should have exactly 5 middleware components
    assert len(middleware_list) == 5

    # Verify order (FIFO)
    assert isinstance(middleware_list[0], LoggingMiddleware)
    assert isinstance(middleware_list[1], TimingMiddleware)
    assert isinstance(middleware_list[2], RateLimitingMiddleware)
    assert isinstance(middleware_list[3], ErrorHandlingMiddleware)
    assert isinstance(middleware_list[4], CachingMiddleware)

