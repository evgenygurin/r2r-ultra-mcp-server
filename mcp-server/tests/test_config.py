"""
Tests for server configuration and environment variables.
"""


def test_environment_variables():
    """Test that environment variables are properly configured."""
    from server import MAX_RETRIES, R2R_BASE_URL, TIMEOUT

    # R2R_BASE_URL should have a default or be set
    assert R2R_BASE_URL is not None
    assert isinstance(R2R_BASE_URL, str)

    # MAX_RETRIES should be an integer
    assert isinstance(MAX_RETRIES, int)
    assert MAX_RETRIES >= 0

    # TIMEOUT should be a float
    assert isinstance(TIMEOUT, float)
    assert TIMEOUT > 0


def test_server_version():
    """Test server version information."""
    from server import mcp

    assert "v3.0" in mcp.name
    assert "R2R Ultra MCP Server" in mcp.name


def test_server_instructions():
    """Test that server has comprehensive instructions."""
    from server import mcp

    instructions = mcp._instructions
    assert instructions is not None
    assert len(instructions) > 0

    # Check for key features mentioned
    assert "middleware" in instructions.lower()
    assert "tools" in instructions.lower()
    assert "features" in instructions.lower()

