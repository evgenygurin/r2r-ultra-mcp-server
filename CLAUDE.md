# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Обзор проекта

Репозиторий содержит русскоязычную документацию для трех ключевых технологий AI-разработки:

- **R2R** (RAG to Riches) - production-ready система retrieval-augmented generation с vector search, knowledge graphs и agentic RAG
- **FastMCP** - Pythonic фреймворк для создания серверов и клиентов Model Context Protocol (MCP)
- **Claude Code** - официальный CLI инструмент от Anthropic для агентного программирования

## 📁 Структура проекта

```text
r2r-fastmcp/
├── README.md                         # Главная страница (пустая)
├── docs/
│   ├── r2r/                         # 8 файлов: от установки до агентов
│   │   ├── README.md                # Обзор и quick start
│   │   └── 01-08-*.md              # Тематические разделы
│   ├── fastmcp/                     # 8 файлов: от введения до интеграций
│   │   ├── README.md                # Навигация по документации
│   │   └── 01-08-*.md              # Тематические разделы
│   └── claude_code/                 # 13 файлов: полное руководство
│       ├── README.md                # Структура документации
│       ├── SUMMARY.md              # Краткое содержание
│       └── 01-13-*.md              # Тематические разделы
```

## 🔍 Характер проекта

**Это репозиторий ДОКУМЕНТАЦИИ, а не кода.**

- Нет исходного кода для компиляции или тестирования
- Нет зависимостей для установки (нет pyproject.toml, package.json)
- Нет build commands или CI/CD пайплайнов
- Все файлы - это markdown документация на русском языке

## ✏️ Работа с документацией

### Редактирование существующих файлов

```bash
# Поиск по содержимому
rg "search term" docs/

# Поиск файлов по паттерну
fd -e md . docs/

# Открыть конкретный файл
# Используй Read tool для чтения перед редактированием
```

### Структура разделов документации

Каждая технология имеет стандартную структуру:

**R2R** (8 разделов):
1. Installation and Setup
2. Document Management
3. Search and RAG
4. Knowledge Graphs
5. Collections
6. Authentication and Users
7. Configuration
8. Agent

**FastMCP** (8 разделов):
1. Introduction
2. Tools
3. Resources & Prompts
4. Client & Connection
5. Authentication
6. Deployment & Configuration
7. Middleware & Error Handling
8. FastAPI & OpenAPI Integration

**Claude Code** (13 разделов):
1. Overview and Getting Started
2. Installation and Setup
3. Core Features
4. Commands and Usage
5. Hooks and Customization
6. Subagents
7. MCP Integration
8. Skills and Agents
9. Plugins and Marketplaces
10. Settings and Configuration
11. GitHub Integration
12. Security and Permissions
13. Troubleshooting and Debugging

### Форматирование

- **Язык**: Русский (основной текст), английский (код, технические термины)
- **Стиль кода**: Использовать блоки с указанием языка (```python, ```bash, ```json)
- **Заголовки**: Эмодзи в H2 заголовках для улучшения навигации (🎯, 📁, 🔍, etc.)
- **Ссылки**: Относительные пути для внутренней навигации

### Типичные задачи

#### Добавление нового раздела в документацию

```bash
# 1. Определи номер следующего раздела
fd -e md . docs/fastmcp/ | sort

# 2. Создай файл с соответствующим номером
# 3. Обнови README.md и/или SUMMARY.md со ссылкой на новый раздел
# 4. Убедись, что структура соответствует другим разделам
```

#### Обновление README файлов

```bash
# Каждая директория docs/*/README.md служит навигационным хабом
# При добавлении нового раздела обновляй:
# - Содержание (table of contents)
# - Быстрые ссылки
# - Рекомендуемый порядок изучения (если применимо)
```

#### Проверка внутренних ссылок

```bash
# Найди все markdown ссылки
rg '\[.*\]\(\..*\.md.*\)' docs/

# Проверь, что целевые файлы существуют
# Относительные пути должны работать из директории файла
```

## 🎨 Стандарты качества документации

### Обязательные элементы раздела

1. **Четкий заголовок** с эмодзи
2. **Введение** - что охватывает раздел (2-3 предложения)
3. **Практические примеры** с кодом
4. **Best Practices** - рекомендации и предупреждения
5. **Следующие шаги** - ссылки на связанные разделы

### Качество примеров кода

- **Полнота**: Примеры должны быть runnable (даже если это документация)
- **Комментарии**: Объясняй неочевидные моменты
- **Консистентность**: Используй единые стили кода внутри документа
- **Актуальность**: Проверяй соответствие последним версиям API

### Язык и терминология

- **Технические термины**: Оставляй на английском (MCP, RAG, JWT, etc.)
- **API endpoints**: Всегда в оригинале
- **Команды**: В кодовых блоках на английском
- **Объяснения**: На русском с сохранением терминов

## 🚫 Запрещенные действия

1. **НЕ создавай** build scripts, CI/CD конфиги, test files - это репозиторий документации
2. **НЕ добавляй** package.json, pyproject.toml, requirements.txt - нет кодовой базы
3. **НЕ предлагай** автоматизацию тестирования примеров кода - это справочная документация
4. **НЕ меняй** язык документации на английский без явного запроса
5. **НЕ удаляй** эмодзи из заголовков - это часть стиля документации

## 💡 Полезные команды

### Поиск и навигация

```bash
# Найти упоминания конкретной функции/API
rg "client.documents.create" docs/

# Найти все примеры на Python
rg "```python" docs/

# Найти разделы про аутентификацию
fd -e md authentication docs/

# Подсчитать количество примеров кода в разделе
rg "```" docs/r2r/ | wc -l
```

### Валидация структуры

```bash
# Проверить наличие всех файлов в директории
fd -e md . docs/fastmcp/ | sort

# Найти неработающие относительные ссылки (базовая проверка)
rg '\[.*\]\(\./.*\.md\)' docs/ | sed 's/.*(\.\///' | sed 's/).*//' | while read f; do [ -f "docs/$f" ] || echo "Missing: $f"; done
```

### Статистика

```bash
# Общее количество разделов
fd -e md . docs | wc -l

# Размер документации по технологиям
du -sh docs/r2r docs/fastmcp docs/claude_code

# Количество примеров кода
rg -c "```" docs/**/*.md
```

## 🎯 Workflow для типичных задач

### Обновление существующего раздела

1. **Читай перед редактированием**: ВСЕГДА используй Read tool
2. **Сохраняй структуру**: Не меняй порядок разделов без необходимости
3. **Проверяй ссылки**: Убедись, что внутренние ссылки остались валидными
4. **Обновляй содержание**: Если меняешь заголовки, обнови table of contents

### Добавление нового раздела

1. **Изучи существующие**: Пойми текущую структуру и стиль
2. **Выбери правильный номер**: Следуй последовательной нумерации (01-XX)
3. **Используй шаблон**: Скопируй структуру из похожего раздела
4. **Обнови индекс**: Добавь ссылки в README.md и SUMMARY.md (если есть)
5. **Проверь навигацию**: Добавь "Следующие шаги" в конец

### Рефакторинг документации

1. **Не разрушай навигацию**: При переименовании обнови ВСЕ ссылки
2. **Сохраняй нумерацию**: Не меняй номера файлов без глобального рефакторинга
3. **Git friendly**: Используй git mv для переименования файлов
4. **Консистентность**: Синхронизируй изменения между README и SUMMARY

## 📚 Контекст технологий

### R2R
- **Назначение**: Production RAG система
- **Ключевые концепты**: Documents, Collections, Knowledge Graphs, Vector Search
- **API**: REST v3, Python SDK, JavaScript SDK
- **Deployment**: Docker, PostgreSQL + pgvector

### FastMCP
- **Назначение**: Создание MCP серверов и клиентов
- **Ключевые концепты**: Tools, Resources, Prompts, Authentication, Middleware
- **Паттерны**: Декораторы (@mcp.tool), Context injection, FastAPI интеграция
- **Deployment**: FastMCP Cloud, HTTP, Stdio

### Claude Code
- **Назначение**: CLI для агентного программирования
- **Ключевые концепты**: Subagents, Hooks, Skills, MCP Integration, CLAUDE.md
- **Кастомизация**: Slash commands, Hooks, Plugins, Settings
- **Интеграция**: GitHub, VS Code, MCP servers

---

## 📋 R2R Quick Reference

### API Endpoints

#### Documents `/v3/documents`
- `POST /v3/documents` - Создать документ
- `GET /v3/documents` - Список документов
- `GET /v3/documents/{id}` - Получить документ
- `DELETE /v3/documents/{id}` - Удалить документ
- `POST /v3/documents/{id}/extract` - Извлечение Knowledge Graph

#### Retrieval `/v3/retrieval`
- `POST /v3/retrieval/search` - Поиск (semantic, fulltext, hybrid)
- `POST /v3/retrieval/rag` - RAG-запрос с генерацией
- `POST /v3/retrieval/agent` - Агент с multi-turn conversations

#### Collections `/v3/collections`
- `POST /v3/collections` - Создать коллекцию
- `GET /v3/collections` - Список коллекций
- `POST /v3/collections/{id}/documents` - Добавить документ
- `POST /v3/collections/{id}/users/{user_id}` - Добавить пользователя

#### Knowledge Graphs `/v3/graphs`
- `POST /v3/graphs/{collection_id}/pull` - Синхронизация графа
- `POST /v3/graphs/{collection_id}/entities` - Создать сущность
- `POST /v3/graphs/{collection_id}/relationships` - Создать связь
- `POST /v3/graphs/{collection_id}/communities/build` - Построить сообщества

#### Users `/v3/users`
- `POST /v3/users` - Регистрация
- `POST /v3/users/login` - Вход
- `GET /v3/users/me` - Текущий пользователь
- `POST /v3/users/{id}/api_keys` - Создать API ключ

### Python SDK

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Аутентификация
client.register("user@example.com", "password")
client.login("user@example.com", "password")

# Документы
client.documents.create(file_path="document.pdf")
client.documents.create(file_path="doc.pdf", collection_ids=[collection_id])
client.documents.list()

# Поиск
results = client.retrieval.search(query="What is ML?")
results = client.retrieval.search(
    query="query",
    search_settings={
        "use_hybrid_search": True,
        "filters": {"collection_ids": {"$overlap": [collection_id]}}
    }
)

# RAG
response = client.retrieval.rag(
    query="Explain neural networks",
    rag_generation_config={"model": "openai/gpt-4.1", "temperature": 0.7}
)

# Agent
response = client.retrieval.agent(
    message={"role": "user", "content": "What is DeepSeek R1?"},
    mode="research",  # или "rag"
    conversation_id=conversation_id
)

# Коллекции
collection = client.collections.create("Research Papers")
client.collections.add_document(collection_id, document_id)
client.collections.add_user(user_id, collection_id)

# Knowledge Graphs
client.graphs.pull(collection_id)
client.graphs.build_communities(collection_id)
entities = client.graphs.list_entities(collection_id)
```

### JavaScript SDK

```javascript
import { R2RClient } from 'r2r-js';

const client = new R2RClient('http://localhost:7272');

// Документы
await client.documents.create({
    file: { path: 'document.pdf', name: 'document.pdf' },
    metadata: { title: 'My Document' }
});

// RAG
const response = await client.rag({
    query: 'What does the file talk about?',
    rag_generation_config: {
        model: 'openai/gpt-4.1',
        temperature: 0.0,
        stream: false
    }
});

// Agent
const response = await client.agent({
    message: { role: 'user', content: 'Query' },
    search_mode: 'advanced'
});
```

### Конфигурация r2r.toml

```toml
[app]
default_max_documents_per_user = 100
fast_llm = "openai/gpt-4.1-mini"
quality_llm = "openai/gpt-4.1"

[auth]
provider = "r2r"
access_token_lifetime_in_minutes = 60
require_authentication = true

[completion]
provider = "litellm"
  [completion.generation_config]
  model = "openai/gpt-4.1"
  temperature = 0.1

[embedding]
provider = "litellm"
base_model = "openai/text-embedding-3-small"
base_dimension = 512

[ingestion]
chunking_strategy = "recursive"
chunk_size = 1024
chunk_overlap = 512

[database.graph_creation_settings]
entity_types = ["Person", "Organization", "Location"]
relation_types = ["works_at", "located_in"]
max_knowledge_relationships = 100
```

### Search Modes & Strategies

**Modes:**
- `basic` - Простой semantic search
- `advanced` - Hybrid (semantic + fulltext)
- `custom` - Полный контроль через `search_settings`

**Strategies:**
- `vanilla` - Стандартный semantic search
- `rag_fusion` - Multiple queries + Reciprocal Rank Fusion
- `hyde` - Hypothetical Document Embeddings

### Filter Operators

| Оператор | Описание | Пример |
|----------|----------|--------|
| `$eq` | Равно | `{"status": {"$eq": "active"}}` |
| `$neq` | Не равно | `{"status": {"$neq": "deleted"}}` |
| `$gt` / `$gte` | Больше / больше или равно | `{"year": {"$gte": 2020}}` |
| `$lt` / `$lte` | Меньше / меньше или равно | `{"score": {"$lt": 100}}` |
| `$in` | В списке | `{"category": {"$in": ["tech", "ai"]}}` |
| `$overlap` | Пересечение массивов | `{"tags": {"$overlap": ["python"]}}` |
| `$and` / `$or` | Логические операторы | `{"$and": [{...}, {...}]}` |

### Docker Commands

```bash
# Базовый запуск
git clone git@github.com:SciPhi-AI/R2R.git && cd R2R
export OPENAI_API_KEY=sk-...
docker compose up

# Full mode с PostgreSQL
export R2R_CONFIG_NAME=full
docker compose -f compose.full.yaml --profile postgres up -d

# Проверка
curl http://localhost:7272/v3/system/settings
```

### Environment Variables

```bash
export OPENAI_API_KEY=sk-...
export R2R_CONFIG_PATH=/path/to/r2r.toml
export R2R_CONFIG_NAME=full
export POSTGRES_HOST=localhost
export R2R_BASE_URL=http://localhost:7272
```

---

## 📋 FastMCP Quick Reference

### Декораторы

#### @mcp.tool - Создание инструментов

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

# Базовый декоратор
@mcp.tool
def add(a: int, b: int) -> int:
    """Складывает два числа."""
    return a + b

# С кастомным именем
@mcp.tool("custom_name")
def my_tool(x: int) -> str:
    return str(x)

# С расширенной конфигурацией
from fastmcp.server.decorators import ToolAnnotations

@mcp.tool(
    name="important_tool",
    description="Критически важный инструмент",
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
    ),
    exclude_args=['internal_param'],  # Скрытые параметры
    meta={"version": "2.0"}            # Метаданные
)
def important_tool() -> str:
    return "Done"
```

#### @mcp.resource - Создание ресурсов

```python
# Базовый ресурс
@mcp.resource("config://settings")
def get_settings() -> str:
    return "key=value"

# Ресурс с параметрами (URI template)
@mcp.resource("users://{user_id}/profile")
def get_profile(user_id: str) -> str:
    return f"Profile for {user_id}"

# С метаданными
@mcp.resource(
    "data://report",
    name="Analytics Report",
    description="Ежедневный отчет",
    mime_type="application/json",
    tags={"analytics", "reports"}
)
def get_report() -> str:
    return '{"data": []}'
```

#### @mcp.prompt - Создание промптов

```python
# Простой промпт
@mcp.prompt
def greeting(name: str) -> str:
    return f"Hello, {name}!"

# Промпт с множественными сообщениями
@mcp.prompt
def analysis_prompt(topic: str) -> list[dict]:
    return [
        {"role": "system", "content": f"You are an expert in {topic}"},
        {"role": "user", "content": f"Analyze {topic}"}
    ]
```

### Context API

```python
from fastmcp import Context

@mcp.tool
async def advanced_tool(query: str, ctx: Context) -> dict:
    """Tool с доступом к MCP контексту."""

    # Доступ к ресурсам
    resources = await ctx.list_resources()
    content = await ctx.read_resource("resource://config")

    # Доступ к tools и prompts
    tools = await ctx.list_tools()
    prompts = await ctx.list_prompts()

    # Доступ к access token (для аутентификации)
    token = ctx.access_token
    if token:
        user_id = token.sub
        scopes = token.scopes

    return {"query": query, "resources": len(resources)}
```

**Важно о Context:**
- Имя параметра не важно, важен type hint `Context`
- Позиция параметра не важна
- Context опционален
- Методы Context асинхронны

### Транспорты

```python
# Server
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

# HTTP (для production)
mcp.run(transport="http", host="0.0.0.0", port=8000)

# Stdio (для локального использования)
mcp.run(transport="stdio")

# Client
from fastmcp import Client

# HTTP Transport
client = Client("http://localhost:8000/mcp")

# Stdio Transport
client = Client("my_server.py")

# In-memory (тестирование)
client = Client(server)

# Использование
async with client:  # ОБЯЗАТЕЛЬНО контекстный менеджер
    # Tools
    tools = await client.list_tools()
    result = await client.call_tool("add", {"a": 5, "b": 3})

    # Resources
    resources = await client.list_resources()
    content = await client.read_resource("config://settings")

    # Prompts
    prompts = await client.list_prompts()
    prompt = await client.get_prompt("greeting", {"name": "User"})
```

### Middleware Hooks

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class LoggingMiddleware(Middleware):
    async def on_request(self, context: MiddlewareContext, call_next):
        """Для всех запросов."""
        return await call_next(context)

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """При вызове tool."""
        tool_name = context.message.name
        logging.info(f"Tool call: {tool_name}")
        return await call_next(context)

    async def on_read_resource(self, context: MiddlewareContext, call_next):
        """При чтении resource."""
        return await call_next(context)

    async def on_get_prompt(self, context: MiddlewareContext, call_next):
        """При получении prompt."""
        return await call_next(context)

mcp.add_middleware(LoggingMiddleware())
```

### Аутентификация

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers import JWTVerifier

# Асимметричная (JWKS)
auth = JWTVerifier(
    jwks_url="https://domain.auth0.com/.well-known/jwks.json",
    issuer="https://domain.auth0.com/",
    audience="your-api-identifier",
    algorithms=["RS256"],
    required_scopes=["read:data", "write:data"]
)

# Симметричная (HMAC)
auth = JWTVerifier(
    public_key="your-shared-secret-key-min-32-chars",
    algorithms=["HS256"],
    issuer="your-service"
)

mcp = FastMCP("Secure Server", auth_provider=auth)
```

### Конфигурация fastmcp.json

```json
{
  "source": {
    "entrypoint": "server.py:mcp",
    "path": "./src",
    "watch": ["*.py"]
  },
  "environment": {
    "python": "3.11",
    "dependencies": "requirements.txt",
    "system_packages": ["git"]
  },
  "deployment": {
    "transport": "http",
    "host": "0.0.0.0",
    "port": 8000,
    "env": {
      "API_KEY": "${API_KEY}",
      "DATABASE_URL": "${DATABASE_URL}"
    }
  }
}
```

**Запуск:**
```bash
fastmcp run fastmcp.json
fastmcp run fastmcp.json --port 9000  # Override
```

### Ключевые импорты

```python
# Основные
from fastmcp import FastMCP, Client, Context

# Аутентификация
from fastmcp.server.auth.providers import JWTVerifier, AWSCognitoProvider

# Middleware
from fastmcp.server.middleware import Middleware, MiddlewareContext

# Ресурсы
from fastmcp.resources import TextResource, FileResource, DirectoryResource

# Транспорты
from fastmcp.client.transports import StreamableHttpTransport, StdioTransport

# Исключения
from fastmcp.exceptions import ToolError, ResourceError, PromptError

# Декораторы
from fastmcp.server.decorators import ToolAnnotations
```

---

## 📋 Claude Code Quick Reference

### CLI & Флаги

```bash
claude                      # REPL (интерактивный режим)
claude "prompt"             # One-shot команда
claude --debug              # Debug режим
claude --verbose            # Подробный вывод
claude --file path          # С файлом контекста
claude --max-budget-usd N   # Ограничение бюджета
claude --model <name>       # Выбор модели
claude --no-cache           # Без кэша
claude --headless           # Без интерактивности
```

### Slash Commands

#### Управление сессией
- `/help` - Справка по всем командам
- `/resume` - Продолжить предыдущую сессию
- `/clear` - Очистить контекст
- `/exit`, `/quit` - Выйти
- `/compact` - Сжатие контекста

#### Контекст
- `/context` - Показать текущий контекст (файлы, токены)
- `/add <path>` - Добавить файл в контекст
- `/remove <path>` - Удалить файл из контекста

#### Конфигурация
- `/config` - Открыть интерфейс настроек
- `/permissions` - Управление разрешениями
- `/model <name>` - Переключить модель
- `/mcp` - Управление MCP серверами

#### Файлы
- `/read <path>` - Прочитать файл
- `/write <path>` - Создать/перезаписать файл
- `/search <query>` - Поиск в директории

#### Git
- `/git status` - Статус репозитория
- `/git diff` - Текущие изменения
- `/git log` - История коммитов

#### Debug
- `/debug on|off` - Режим отладки
- `/logs` - Логи сессии
- `/health` - Статус сервисов
- `/doctor` - Диагностика системы
- `/bug` - Создание bug report

#### Plugins
- `/plugin install <name>` - Установить plugin
- `/plugin list` - Список plugins
- `/plugin enable|disable <name>` - Включить/отключить
- `/plugin marketplace` - Просмотр marketplace

### Hooks (7 типов)

| Тип | Когда срабатывает | Пример использования |
|-----|-------------------|---------------------|
| **SessionStart** | Старт сессии | npm install, docker-compose up |
| **SessionEnd** | Завершение сессии | Очистка, остановка сервисов |
| **PreToolUse** | Перед tool | Валидация команд, логирование |
| **PostToolUse** | После tool | Auto-format, lint, тесты |
| **Stop** | Запрос остановки | Prompt-based проверка |
| **SubagentStart** | Запуск субагента | Контроль запуска |
| **SubagentStop** | Остановка субагента | Контроль завершения |

**Конфигурация hooks (settings.json):**
```json
{
  "hooks": [{
    "event": "PostToolUse",
    "matcher": "Edit",
    "hooks": [{
      "type": "command",
      "command": "ruff format $FILE",
      "description": "Auto-format Python files"
    }]
  }]
}
```

**Переменные hooks:**
- `$CLAUDE_TOOL_NAME` - имя инструмента
- `$CLAUDE_TOOL_INPUT` - JSON входных данных
- `$CLAUDE_TOOL_OUTPUT` - результат (PostToolUse)
- `$FILE` - путь к файлу (для Edit)

### Субагенты (9 типов)

| Субагент | Назначение | Модель |
|----------|------------|--------|
| **Explore** | Быстрое исследование кодовой базы | Haiku 4.5 |
| **Plan** | Планирование сложных задач | Sonnet→Haiku |
| **Code Explorer** | Глубокий анализ кода | - |
| **Code Architect** | Проектирование (2-3 подхода) | - |
| **Code Reviewer** | Проверка качества (confidence 0-100) | - |
| **Silent Failure Hunter** | Поиск тихих ошибок | - |
| **PR Test Analyzer** | Покрытие тестами | - |
| **Comment Analyzer** | Проверка документации | - |
| **Code Simplifier** | Полировка кода | - |

**Параллельное выполнение:** до 4 агентов одновременно

### Settings.json структура

**Расположение:**
- `~/.claude/settings.json` - глобальные
- `.claude/settings.json` - проектные (приоритет выше)

```json
{
  "permissions": {
    "allowedTools": [
      "Read(**/*.{js,ts,json,md})",
      "Edit(**/*.{js,ts})",
      "Bash(git:*)",
      "Bash(npm:*)"
    ],
    "deniedTools": [
      "Edit(/config/secrets.json)",
      "Bash(rm -rf:*)"
    ]
  },
  "permissionMode": "acceptEdits",  // acceptEdits | manual | strict
  "sandbox": {
    "allowUnsandboxedCommands": false
  },
  "hooks": [...],
  "mcpServers": {...},
  "statusLine": {
    "enabled": true,
    "format": "{{model}} | {{tokens}}"
  }
}
```

**Permission Modes:**
- `acceptEdits` - Автоматическое применение правок
- `manual` - Подтверждение каждого Edit
- `strict` - Только явно указанные в allowedTools

### Официальные MCP серверы

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-github"],
      "oauth": {
        "clientId": "${GITHUB_CLIENT_ID}",
        "clientSecret": "${GITHUB_CLIENT_SECRET}",
        "scopes": ["repo", "issues"]
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

**Серверы:**
- `@anthropic-ai/mcp-server-github` - GitHub
- `@modelcontextprotocol/server-filesystem` - Файловая система
- `@modelcontextprotocol/server-postgres` - PostgreSQL
- `@modelcontextprotocol/server-slack` - Slack

### Официальные Plugins

| Plugin | Описание |
|--------|----------|
| **pr-review-toolkit** | 6 агентов для code review |
| **commit-commands** | /commit, /commit-push, /commit-push-pr |
| **feature-dev** | 7-фазный workflow разработки |
| **code-review** | Автоматический PR review |
| **agent-sdk-development** | Scaffold SDK проектов |

**Команды управления:**
```bash
/plugin install pr-review-toolkit
/plugin enable pr-review-toolkit
/plugin list
/plugin marketplace
```

### Environment Variables

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-5
export CLAUDE_BASH_NO_LOGIN=1
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
export DISABLE_AUTOUPDATER=1
```

---

## 🔗 Интеграции между технологиями

### FastMCP + Claude Code

FastMCP серверы могут быть подключены к Claude Code как MCP серверы для расширения возможностей:

**Конфигурация (settings.json):**
```json
{
  "mcpServers": {
    "my-fastmcp-server": {
      "command": "python",
      "args": ["path/to/server.py"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**Использование в Claude Code:**
```bash
# После подключения MCP сервера, tools становятся доступны:
@my-fastmcp-server tool_name arg1 arg2

# Или через natural language:
"Use my-fastmcp-server to search documents"
```

**Пример FastMCP сервера для Claude Code:**
```python
from fastmcp import FastMCP

mcp = FastMCP("Development Tools")

@mcp.tool
def run_tests(test_path: str) -> str:
    """Запускает тесты для указанного пути."""
    import subprocess
    result = subprocess.run(["pytest", test_path], capture_output=True)
    return result.stdout.decode()

@mcp.resource("docs://project")
def get_docs() -> str:
    """Возвращает проектную документацию."""
    return open("README.md").read()

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### R2R + FastMCP

R2R может служить backend'ом для FastMCP tools, предоставляя RAG и knowledge graph возможности:

```python
from r2r import R2RClient
from fastmcp import FastMCP, Context

mcp = FastMCP("R2R Knowledge Tools")
r2r_client = R2RClient("http://localhost:7272")

@mcp.tool
async def search_knowledge(query: str, limit: int = 5) -> str:
    """Поиск в knowledge base через R2R."""
    results = r2r_client.retrieval.search(
        query=query,
        search_settings={"limit": limit, "use_hybrid_search": True}
    )
    return str(results)

@mcp.tool
async def ask_question(question: str, ctx: Context) -> str:
    """RAG-запрос к knowledge base."""
    response = r2r_client.retrieval.rag(
        query=question,
        rag_generation_config={"temperature": 0.1}
    )
    return response["generated_text"]

@mcp.tool
async def search_entities(entity_name: str, collection_id: str) -> str:
    """Поиск сущностей в knowledge graph."""
    entities = r2r_client.graphs.list_entities(
        collection_id=collection_id,
        entity_name=entity_name
    )
    return str(entities)

@mcp.resource("knowledge://collections")
def list_collections() -> str:
    """Список доступных коллекций."""
    collections = r2r_client.collections.list()
    return str(collections)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

### R2R + Claude Code (через MCP)

Использование R2R напрямую из Claude Code через FastMCP bridge:

**1. Создать FastMCP bridge (r2r_bridge.py):**
```python
# Код из примера выше
```

**2. Конфигурация в settings.json:**
```json
{
  "mcpServers": {
    "r2r-knowledge": {
      "command": "python",
      "args": ["r2r_bridge.py"],
      "env": {
        "R2R_BASE_URL": "http://localhost:7272"
      }
    }
  }
}
```

**3. Использование в Claude Code:**
```bash
# Поиск в документах
@r2r-knowledge search_knowledge "machine learning algorithms"

# RAG запрос
@r2r-knowledge ask_question "What is transfer learning?"

# Работа с knowledge graph
@r2r-knowledge search_entities "neural networks" collection_id
```

### Полный стек: R2R + FastMCP + Claude Code

**Архитектура:**
```text
┌─────────────────┐
│  Claude Code    │  CLI для разработки
│  (Frontend)     │
└────────┬────────┘
         │ MCP Protocol
         │
┌────────▼────────┐
│    FastMCP      │  MCP сервер (bridge)
│   (Middleware)  │
└────────┬────────┘
         │ Python SDK / REST API
         │
┌────────▼────────┐
│      R2R        │  RAG система (backend)
│   (Backend)     │
└─────────────────┘
```

**Use Cases:**
1. **Code Documentation Search**: Поиск по проектной документации через R2R
2. **Context-Aware Development**: RAG для получения релевантного контекста
3. **Knowledge Graph Navigation**: Исследование связей между концепциями
4. **Intelligent Code Review**: Использование historical knowledge для review

## 🔄 Git Workflow

```bash
# Коммиты всегда одной строкой, без подписей
git add docs/r2r/05-collections.md
git commit -m "docs(r2r): add collection permissions section"

# Типы коммитов для документации
# docs: обновление документации
# fix: исправление ошибок в примерах/ссылках
# refactor: реорганизация структуры
# feat: добавление нового раздела/технологии
```

## ⚡ Best Practices

1. **Используй инструменты поиска**: `rg`, `fd` вместо ручного browse
2. **Читай README первым**: Каждая директория имеет навигационный README
3. **Сохраняй стиль**: Повторяй форматирование существующих разделов
4. **Примеры должны учить**: Не просто показывай синтаксис, объясняй ПОЧЕМУ
5. **Актуальность API**: При обновлении проверяй версии библиотек
6. **Относительные ссылки**: Используй `./` для внутренних ссылок в документации

## 🎓 Полезные паттерны

### Структура примера кода с объяснением

```markdown
### Заголовок функциональности

Краткое описание (1-2 предложения).

```python
# Комментарий, объясняющий ПОЧЕМУ, а не ЧТО
code_example = "with context"
```

**Важно:** Предупреждение или best practice.
```text

### Структура раздела README

```markdown
# Technology Name

Brief overview (1 paragraph).

## Содержание документации

### 1. [Section Title](./01-section.md)
Brief description of section content.

**Key Topics:**
- Topic 1
- Topic 2
```

## 🔮 Когда нужна помощь

Если сомневаешься в:
- **Структуре**: Смотри аналогичные разделы в других технологиях
- **Стиле**: Читай существующие файлы для консистентности
- **Терминологии**: Оставляй технические термины на английском
- **API актуальности**: Предупреждай, что нужна валидация с официальной документацией

## 🎯 Ключевые принципы

1. **Документация для людей**: Пиши понятно, с примерами
2. **Структура важна**: Не ломай навигацию и нумерацию
3. **Консистентность**: Следуй существующему стилю
4. **Практичность**: Примеры должны быть применимыми
5. **Актуальность**: Указывай версии технологий

---

**Тип проекта**: Образовательная документация
**Язык**: Русский (текст) + English (код, термины)
**Формат**: Markdown
**Версии**: R2R v3.x, FastMCP 2.x, Claude Code 1.0.58+
