# Tests for R2R Ultra MCP Server

Comprehensive test suite for the R2R Ultra MCP Server v3.0.

## Test Structure

```
tests/
├── __init__.py           # Test package initialization
├── conftest.py           # Pytest fixtures and configuration
├── test_server.py        # Server initialization and component tests
├── test_middleware.py    # Middleware functionality tests
├── test_config.py        # Configuration and environment tests
└── README.md             # This file
```

## Running Tests

### Install Test Dependencies

```bash
cd /Users/laptop/dev/r2r-fastmcp/mcp-server

# Install with dev dependencies
uv sync
# or
pip install -e ".[dev]"
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=server --cov-report=html

# Run specific test file
pytest tests/test_server.py

# Run specific test
pytest tests/test_server.py::test_server_initialization
```

### Run Tests in Watch Mode

```bash
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw
```

## Test Categories

### 1. Server Tests (`test_server.py`)

Tests for server initialization and core functionality:
- Server initialization
- Tool registration
- Resource registration  
- Prompt registration
- Middleware configuration

### 2. Middleware Tests (`test_middleware.py`)

Tests for middleware components:
- LoggingMiddleware
- TimingMiddleware
- RateLimitingMiddleware
- ErrorHandlingMiddleware
- CachingMiddleware
- Middleware order and integration

### 3. Configuration Tests (`test_config.py`)

Tests for configuration and environment:
- Environment variables
- Server version information
- Server instructions

## Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

### Example Test

```python
def test_my_feature(mcp_server):
    """Test description."""
    # Arrange
    expected_value = "test"
    
    # Act
    result = mcp_server.some_method()
    
    # Assert
    assert result == expected_value
```

### Using Fixtures

```python
def test_with_fixture(mcp_server, mock_r2r_response):
    """Test using fixtures from conftest.py."""
    assert mcp_server is not None
    assert mock_r2r_response is not None
```

## Test Coverage

Current test coverage:
- Server initialization: ✅
- Tools registration: ✅
- Resources registration: ✅
- Prompts registration: ✅
- Middleware initialization: ✅
- Middleware order: ✅
- Configuration: ✅

## CI/CD Integration

Tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -e ".[dev]"
    pytest --cov=server --cov-report=xml
```

## Troubleshooting

### Import Errors

If you get import errors, make sure the parent directory is in PYTHONPATH:

```bash
export PYTHONPATH=/Users/laptop/dev/r2r-fastmcp/mcp-server:$PYTHONPATH
pytest
```

### Environment Variables

Tests use default values for environment variables. To test with specific values:

```bash
R2R_BASE_URL=http://test.example.com pytest
```

### Missing Dependencies

Install test dependencies:

```bash
pip install pytest pytest-asyncio pytest-cov pytest-mock
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Use Fixtures**: Reuse common setup via fixtures
3. **Clear Names**: Test names should describe what they test
4. **Arrange-Act-Assert**: Follow AAA pattern
5. **Mock External Calls**: Don't make real API calls in tests
6. **Fast Tests**: Keep tests fast (<1s per test)

## Contributing

When adding new features:
1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain test coverage above 80%
4. Update this README if adding new test categories

