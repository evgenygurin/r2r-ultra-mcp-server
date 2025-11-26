#!/usr/bin/env python3
"""
Test script to verify all MCP tools work correctly.
Tests the middleware fixes for MiddlewareContext.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the server
from server import mcp


async def test_tools():
    """Test all available tools."""
    
    print("="*80)
    print("🧪 Testing R2R MCP Server Tools")
    print("="*80)
    print()
    
    # Get list of all tools
    tools = await mcp._list_tools()
    print(f"📋 Found {len(tools)} tools:")
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool.name}")
    print()
    
    # Test 1: get_server_capabilities
    print("─" * 80)
    print("Test 1: get_server_capabilities")
    print("─" * 80)
    try:
        from fastmcp import Context
        
        # Create a mock context
        class MockContext:
            request_id = "test-request-1"
            client_id = "test-client"
            
            async def info(self, msg):
                print(f"  ℹ️  {msg}")
            
            async def error(self, msg):
                print(f"  ❌ {msg}")
            
            async def report_progress(self, current, total, message):
                print(f"  📊 Progress: {current}/{total} - {message}")
        
        ctx = MockContext()
        
        # Import the tool function
        from server import get_server_capabilities
        
        result = await get_server_capabilities(ctx)
        
        print(f"✅ Result:")
        print(f"  - Server: {result['server']}")
        print(f"  - Version: {result['version']}")
        print(f"  - R2R URL: {result['r2r_base_url']}")
        print(f"  - Tools: {result['tools_count']}")
        print(f"  - Resources: {result['resources_count']}")
        print(f"  - Prompts: {result['prompts_count']}")
        print(f"  - Middleware: {', '.join(result['features']['middleware'])}")
        print()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    # Test 2: get_performance_stats
    print("─" * 80)
    print("Test 2: get_performance_stats")
    print("─" * 80)
    try:
        from server import get_performance_stats
        
        result = await get_performance_stats()
        
        print(f"✅ Result:")
        print(f"  - Timing operations: {result['timing'].get('total_calls', 0)}")
        print(f"  - Cache hits: {result['cache'].get('hits', 0)}")
        print(f"  - Cache misses: {result['cache'].get('misses', 0)}")
        print(f"  - Cache hit rate: {result['cache'].get('hit_rate', 'N/A')}")
        print(f"  - Rate limit clients: {result['rate_limiting'].get('active_clients', 0)}")
        print(f"  - Total errors: {result['errors'].get('total_errors', 0)}")
        print()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    # Test 3: List resources
    print("─" * 80)
    print("Test 3: List Resources")
    print("─" * 80)
    try:
        resources = await mcp._list_resources()
        print(f"✅ Found {len(resources)} resources:")
        for i, resource in enumerate(resources, 1):
            print(f"  {i}. {resource.uri}")
        print()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print()
    
    # Test 4: List prompts
    print("─" * 80)
    print("Test 4: List Prompts")
    print("─" * 80)
    try:
        prompts = await mcp._list_prompts()
        print(f"✅ Found {len(prompts)} prompts:")
        for i, prompt in enumerate(prompts, 1):
            print(f"  {i}. {prompt.name}")
        print()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print()
    
    # Test 5: Middleware stack
    print("─" * 80)
    print("Test 5: Middleware Stack")
    print("─" * 80)
    try:
        print(f"✅ Middleware configured:")
        for i, middleware in enumerate(mcp._middleware, 1):
            middleware_name = middleware.__class__.__name__
            print(f"  {i}. {middleware_name}")
        print()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print()
    
    print("="*80)
    print("✅ All basic tests completed!")
    print("="*80)
    print()
    print("💡 Note: To test R2R API calls (search, rag, etc.), ensure:")
    print("   1. R2R server is running at the configured URL")
    print("   2. API_KEY is set in .env file")
    print("   3. Run the server with: python server.py")
    print()


if __name__ == "__main__":
    asyncio.run(test_tools())
