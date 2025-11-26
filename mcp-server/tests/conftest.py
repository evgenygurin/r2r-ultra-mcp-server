"""
Pytest configuration and fixtures for R2R Ultra MCP Server tests.
"""
import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mcp_server():
    """Fixture providing the MCP server instance."""
    from server import mcp
    return mcp


@pytest.fixture
def mock_r2r_response():
    """Fixture for mocking R2R API responses."""
    return {
        "results": {
            "chunk_search_results": [
                {
                    "id": "test-chunk-1",
                    "text": "Test content",
                    "score": 0.95,
                    "metadata": {}
                }
            ]
        }
    }

