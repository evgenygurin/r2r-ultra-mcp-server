# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Обзор проекта

**R2R FastMCP Server** — production-ready MCP сервер для интеграции с R2R API. Предоставляет 8+ инструментов через MCP протокол для взаимодействия с R2R (Retrieval & RAG) системой.

**Ключевые характеристики:**
- **FastMCP 2.x** - современный Pythonic фреймворк для MCP
- **Production-grade** - middleware stack (logging, timing, rate limiting, caching, error handling)
- **Async-first** - полностью асинхронная архитектура
- **Три транспорта** - stdio (local), SSE, WebSocket для разных сценариев деплоя

## 📁 Структура проекта

```text
mcp-server/
├── server.py                  # 🚀 Main MCP server (v3.0, production-ready)
├── pyproject.toml             # 📦 Python dependencies (uv/hatch)
├── .env                       # 🔑 R2R credentials (not in git)
├── docs/                      # 📚 Architecture documentation
│   ├── ARCHITECTURE.md        # Two-layer design (Layer1 OpenAPI + Layer2 Smart)
│   ├── COMPARISON.md          # Bash vs MCP comparison
│   ├── DEPLOYMENT.md          # Docker/Systemd/Nginx guides
│   ├── FASTMCP_CLOUD_DEPLOY.md # FastMCP Cloud (recommended)
│   └── QUICK_DEPLOY.md        # 3-minute quick start
└── README.md                  # User-facing documentation
```

## 🔧 Основные команды разработки

### Установка зависимостей

```bash
# Рекомендуется: uv (быстрее pip в 10-100x)
uv sync

# Альтернатива: pip
pip install -e .

# С dev зависимостями (pytest, ruff)
uv sync --extra dev
```

### Запуск сервера

```bash
# Stdio transport (для Cursor/Claude Desktop локально)
python server.py

# Или через fastmcp CLI
fastmcp run server.py

# SSE transport (для удаленного доступа)
python server.py --transport sse --port 8000
fastmcp run server.py --transport sse --port 8000

# WebSocket transport
python server.py --transport ws --port 8000
```

### Тестирование и линтинг

```bash
# Запуск тестов (если есть)
pytest

# Линтинг с Ruff
ruff check .

# Автоисправления
ruff check --fix .

# Форматирование
ruff format .
```

### Конфигурация

Создай `.env` в корне `mcp-server/`:

```bash
R2R_BASE_URL=http://localhost:7272  # Адрес R2R API
API_KEY=your_api_key_here            # Bearer token для аутентификации
MAX_RETRIES=3                        # Retry для HTTP запросов
TIMEOUT=120.0                        # Timeout в секундах
```

**⚠️ ВАЖНО:** `.env` файл содержит credentials и не должен быть в git.

## 🏗️ Архитектура

### Production MCP Server (server.py)

FastMCP сервер с полным enterprise-grade middleware stack:

```python
┌─────────────────────────────────────────────────────┐
│           FastMCP Server (server.py)                │
│                                                     │
│  📊 Lifespan Management                             │
│    - Startup/shutdown hooks                         │
│    - R2R connectivity check                         │
│    - Server statistics tracking                     │
│                                                     │
│  🔄 Middleware Stack (5 layers)                     │
│    1. LoggingMiddleware                             │
│    2. TimingMiddleware                              │
│    3. RateLimitingMiddleware (100 req/min)          │
│    4. ErrorHandlingMiddleware (2 retries)           │
│    5. CachingMiddleware (300s TTL)                  │
│                                                     │
│  🎯 MCP Tools (10+)                                 │
│    - get_server_capabilities()                      │
│    - r2r_search_with_progress()                     │
│    - r2r_rag_with_sampling()                        │
│    - batch_document_analysis()                      │
│    - smart_collection_search()                      │
│    - get_performance_stats()                        │
│    - clear_cache()                                  │
│                                                     │
│  📚 Resources (4+)                                  │
│    - r2r://server/stats                             │
│    - r2r://config                                   │
│    - r2r://collection/{id}/info (template)          │
│    - r2r://document/{id}/summary (template)         │
│                                                     │
│  🎨 Prompts (3+)                                    │
│    - research_question_prompt(topic, depth)         │
│    - code_review_prompt(code, language, focus)      │
│    - data_analysis_prompt(dataset_description)      │
│                                                     │
└─────────────────────────────────────────────────────┘
                        │ HTTP + JSON
                        ▼
┌─────────────────────────────────────────────────────┐
│              R2R API (v3 endpoints)                 │
│         http://localhost:7272/v3/...                │
│                                                     │
│  /v3/retrieval/search  - Hybrid search              │
│  /v3/retrieval/rag     - RAG generation             │
│  /v3/retrieval/agent   - Multi-turn agent           │
│  /v3/collections       - Collection management      │
│  /v3/documents         - Document operations        │
│  /v3/graphs            - Knowledge graph            │
│  /v3/health            - Health check               │
└─────────────────────────────────────────────────────┘
```

### Middleware Stack - Порядок выполнения

**Важно:** Middleware выполняется в порядке добавления (FIFO). В server.py:

```python
mcp.add_middleware(LoggingMiddleware())        # 1. Логирует все запросы
mcp.add_middleware(TimingMiddleware())         # 2. Замеряет время выполнения
mcp.add_middleware(RateLimitingMiddleware())   # 3. Проверяет rate limit
mcp.add_middleware(ErrorHandlingMiddleware())  # 4. Retry логика
mcp.add_middleware(CachingMiddleware())        # 5. Кэширует результаты
```

Request flow: Logging → Timing → RateLimiting → ErrorHandling → Caching → Tool

Response flow: Tool → Caching → ErrorHandling → RateLimiting → Timing → Logging

### Ключевые паттерны FastMCP

#### 1. Lifespan Management

```python
@asynccontextmanager
async def server_lifespan(app):
    # Startup: инициализация, connectivity checks
    logger.info("🚀 Starting...")
    startup_time = datetime.now()

    yield {"stats": server_stats}  # Shared state для middleware/tools

    # Shutdown: cleanup, statistics report
    logger.info("🛑 Shutting down...")
```

#### 2. Context Integration

Все инструменты принимают `Context` для:
- **Логирования**: `await ctx.info()`, `await ctx.error()`
- **Progress reporting**: `await ctx.report_progress(current, total, message)`
- **Metadata**: `ctx.request_id`, `ctx.server`

```python
@mcp.tool()
async def example_tool(param: str, ctx: Context) -> dict:
    await ctx.info(f"Processing: {param}")
    await ctx.report_progress(0, 100, "Starting")
    # ... работа ...
    await ctx.report_progress(100, 100, "Complete")
    return result
```

#### 3. Resource Templates (Parameterized)

```python
@mcp.resource("r2r://collection/{collection_id}/info")
async def collection_info(collection_id: str, ctx: Context) -> str:
    # Параметр {collection_id} становится аргументом функции
    data = await _make_r2r_request("GET", f"/v3/collections/{collection_id}")
    return json.dumps(data, indent=2)
```

#### 4. Custom Middleware Pattern

```python
class CustomMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        # Перед обработкой
        result = await call_next(context)
        # После обработки
        return result

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        # Специфично для tool вызовов
        tool_name = context.request_context.request.params.get("name")
        return await call_next(context)
```

Доступные hooks:
- `on_message()` - все MCP сообщения
- `on_request()` - все запросы
- `on_call_tool()` - только tool вызовы
- `on_list_resources()`, `on_read_resource()` - для ресурсов
- `on_get_prompt()` - для промптов

## 🚀 Deployment

### 1. FastMCP Cloud (Рекомендуется)

**3 шага до production:**

```bash
# 1. Push в GitHub
git push origin main

# 2. Зайти на fastmcp.cloud → Connect Repository

# 3. Configure:
#    - Entry point: server.py:mcp
#    - Environment variables: R2R_BASE_URL, API_KEY
```

**Результат:** `https://your-project.fastmcp.app/mcp`

**Преимущества:**
- ✅ Бесплатно для personal use
- ✅ Автоматический HTTPS/SSL
- ✅ Auto-redeploy на git push
- ✅ Monitoring dashboard
- ✅ PR preview deployments

**Документация:** `docs/FASTMCP_CLOUD_DEPLOY.md`

### 2. Self-hosted (Docker/Systemd/Nginx)

См. подробные инструкции в `docs/DEPLOYMENT.md`:
- Docker Compose для контейнеризации
- Systemd service для always-on Linux servers
- Nginx reverse proxy с SSL/HTTPS
- Environment variables best practices
- Monitoring и logging

### 3. Local Development (Stdio)

**Cursor configuration** (`~/.cursor/settings.json`):

```json
{
  "mcpServers": {
    "r2r": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-server/server.py"],
      "env": {
        "R2R_BASE_URL": "http://localhost:7272",
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "r2r": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-server/server.py"],
      "env": {
        "R2R_BASE_URL": "http://localhost:7272",
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Типичные задачи разработки

### Добавить новый MCP tool

```python
@mcp.tool()
async def my_new_tool(
    param1: str,
    param2: int = 10,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Краткое описание (будет в tool metadata).

    Args:
        param1: Обязательный параметр
        param2: Опциональный с default
        ctx: FastMCP Context для логирования/progress

    Returns:
        Structured JSON response
    """
    if ctx:
        await ctx.info(f"Starting my_new_tool with {param1}")
        await ctx.report_progress(0, 100, "Initializing")

    try:
        # Твоя логика
        result = await _make_r2r_request("POST", "/v3/endpoint", {
            "param": param1,
            "value": param2
        }, ctx)

        if ctx:
            await ctx.report_progress(100, 100, "Complete")

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        if ctx:
            await ctx.error(f"Tool failed: {e}")
        raise
```

**ВАЖНО:**
- Всегда type hints для параметров (нужно для MCP schema generation)
- Docstring обязателен (становится tool description)
- Context опционален но рекомендуется для production tools

### Добавить новый Resource

```python
# Static resource
@mcp.resource("r2r://my-resource")
async def my_resource() -> str:
    """Resource description (shown in list)."""
    data = {"key": "value"}
    return json.dumps(data, indent=2)

# Resource template (parameterized)
@mcp.resource("r2r://entity/{entity_id}/details")
async def entity_details(entity_id: str, ctx: Context) -> str:
    """Get entity details by ID."""
    result = await _make_r2r_request("GET", f"/v3/entities/{entity_id}", ctx=ctx)
    return json.dumps(result, indent=2)
```

### Добавить новый Prompt

```python
@mcp.prompt()
async def my_prompt(
    user_query: str,
    style: str = "concise",
    ctx: Context = None
) -> list[PromptMessage]:
    """
    Generate prompt for specific task.

    Prompts - это reusable templates для LLM запросов.
    """
    if ctx:
        await ctx.info(f"Generating prompt for: {user_query}")

    instruction = f"""
    Task: {user_query}
    Style: {style}

    Please provide a {style} response following these guidelines:
    1. Clear structure
    2. Evidence-based
    3. Actionable insights
    """

    return [PromptMessage(
        role="user",
        content=TextContent(type="text", text=instruction)
    )]
```

### Создать Custom Middleware

```python
class MyCustomMiddleware(Middleware):
    def __init__(self, config_param: str):
        self.config_param = config_param
        self.logger = logging.getLogger("mcp.custom")

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """Intercept tool calls."""
        tool_name = context.request_context.request.params.get("name")

        # Pre-processing
        self.logger.info(f"Tool called: {tool_name}")

        try:
            result = await call_next(context)
            # Post-processing
            return result
        except Exception as e:
            # Error handling
            self.logger.error(f"Tool {tool_name} failed: {e}")
            raise

# Добавить в server
mcp.add_middleware(MyCustomMiddleware("config_value"))
```

### Тестирование MCP Tools локально

```python
# test_tools.py (pytest example)
import pytest
from server import mcp, _make_r2r_request

@pytest.mark.asyncio
async def test_r2r_search():
    # Mock Context
    class MockContext:
        async def info(self, msg): print(f"INFO: {msg}")
        async def error(self, msg): print(f"ERROR: {msg}")
        async def report_progress(self, c, t, m): pass

    ctx = MockContext()

    # Call tool function directly
    result = await r2r_search_with_progress(
        query="test",
        limit=3,
        strategy="hybrid",
        ctx=ctx
    )

    assert result is not None
    assert "results" in result
```

## ⚙️ Конфигурация

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `R2R_BASE_URL` | `http://localhost:7272` | R2R API base URL |
| `API_KEY` | `""` | Bearer token для R2R аутентификации |
| `MAX_RETRIES` | `3` | Количество retry для HTTP запросов |
| `TIMEOUT` | `120.0` | HTTP timeout в секундах |

### Middleware Configuration

Изменить настройки middleware в `server.py:336-342`:

```python
mcp.add_middleware(RateLimitingMiddleware(max_requests_per_minute=100))  # Adjust rate limit
mcp.add_middleware(ErrorHandlingMiddleware(max_retries=2))               # Adjust retries
mcp.add_middleware(CachingMiddleware(ttl=300))                           # Adjust TTL (seconds)
```

### Transport Selection

```python
# В server.py:961 или через CLI
mcp.run()  # Default: stdio

# CLI override
fastmcp run server.py --transport sse --port 8000
python server.py --transport ws --port 9000
```

## 🚫 Запрещенные действия

1. **НЕ коммить** `.env` файл с credentials в git
2. **НЕ изменяй** порядок middleware без понимания последствий (влияет на request/response flow)
3. **НЕ используй** synchronous I/O внутри async функций (blocking operations)
4. **НЕ создавай** tools без type hints (сломает MCP schema generation)
5. **НЕ пропускай** docstrings для tools/resources/prompts (становятся metadata)
6. **НЕ используй** `print()` для логирования - всегда `logger.info()` или `ctx.info()`

## ✅ Обязательные практики

### При добавлении новых tools

1. **Type hints обязательны** для всех параметров и return types
2. **Docstring обязателен** - становится tool description в MCP
3. **Context integration рекомендуется** - используй `ctx: Context` для production tools
4. **Error handling** - используй try/except и `ctx.error()` для отчетов
5. **Progress reporting** - для long-running operations используй `ctx.report_progress()`

### При изменении middleware

1. **Тестируй порядок выполнения** - middleware stack влияет на всю цепочку
2. **Логируй операции** - каждый middleware должен логировать что делает
3. **Не блокируй request chain** - всегда `await call_next(context)`
4. **Handle errors gracefully** - wrap в try/except с proper error reporting

### Git workflow

```bash
# ВСЕГДА одна строка, БЕЗ Co-Authored-By подписей
git commit -m "feat: add new r2r_collections_search tool"
git commit -m "fix: correct timeout handling in middleware"
git commit -m "docs: update deployment guide for FastMCP Cloud"
```

**Типы:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## 📚 Полезные ссылки

### Документация проекта

- `README.md` - User-facing documentation (установка, примеры)
- `docs/ARCHITECTURE.md` - Детальная архитектура (two-layer design)
- `docs/COMPARISON.md` - Bash vs MCP сравнение
- `docs/DEPLOYMENT.md` - Self-hosted deployment guides
- `docs/FASTMCP_CLOUD_DEPLOY.md` - FastMCP Cloud deployment (рекомендуется)
- `docs/QUICK_DEPLOY.md` - Quick start за 3 минуты

### External Documentation

- **FastMCP Docs:** https://github.com/jlowin/fastmcp
- **MCP Specification:** https://modelcontextprotocol.io/
- **R2R API Docs:** https://r2r-docs.sciphi.ai/

## 🔍 Troubleshooting

### "Failed to connect to R2R"

**Причина:** R2R API недоступен или неверный `R2R_BASE_URL`

**Решение:**
```bash
# Проверь R2R health endpoint
curl http://localhost:7272/v3/health

# Проверь .env file
cat .env | grep R2R_BASE_URL

# Убедись что R2R запущен
docker ps | grep r2r  # Если в Docker
```

### "Authentication failed" / 401 Unauthorized

**Причина:** Неверный или отсутствующий `API_KEY`

**Решение:**
```bash
# Проверь API_KEY в .env
cat .env | grep API_KEY

# Проверь что environment variables загружены
python -c "import os; print(os.getenv('API_KEY'))"
```

### Middleware не срабатывает

**Причина:** Неправильный порядок добавления или wrong hook

**Решение:**
- Проверь что middleware добавлен ДО `mcp.run()`
- Используй правильный hook: `on_call_tool` для tools, `on_message` для всех операций
- Всегда `await call_next(context)` в middleware chain

### Cache не работает

**Причина:** TTL истек или cache key collision

**Решение:**
```python
# Очисти cache через tool
await clear_cache()

# Проверь cache stats
await get_performance_stats()

# Увеличь TTL в CachingMiddleware
mcp.add_middleware(CachingMiddleware(ttl=600))  # 10 minutes
```

## 📊 Мониторинг и метрики

### Performance Statistics

```python
# Получить детальную статистику middleware
stats = await get_performance_stats()

# Response содержит:
{
  "timing": {
    "operations": ["tool1", "tool2"],
    "total_calls": 150,
    "average_times": {"tool1": 234.5, "tool2": 123.1}
  },
  "cache": {
    "hits": 45,
    "misses": 105,
    "hit_rate": "30.0%",
    "cache_size": 12
  },
  "rate_limiting": {
    "max_requests_per_minute": 100,
    "active_clients": 3
  },
  "errors": {
    "total_errors": 5,
    "errors_by_type": {"tool1:HTTP500": 2, "tool2:Timeout": 3}
  }
}
```

### Server Capabilities

```python
# Полная информация о сервере и его возможностях
caps = await get_server_capabilities()

# Response включает:
# - R2R health status
# - Enabled features
# - Middleware statistics
# - Tools/resources/prompts count
```

## 🎯 Ключевые принципы

1. **Async-first** - все I/O операции через async/await
2. **Type-safe** - строгая типизация для всех public функций
3. **Context-aware** - используй Context для production tools
4. **Enterprise-grade** - middleware stack для reliability
5. **Pythonic** - следуй FastMCP idioms и best practices
6. **Production-ready** - логирование, мониторинг, error handling из коробки
