# Hooks и Кастомизация Claude Code

## Что такое Hooks?

**Hooks** — это пользовательские shell команды, которые выполняются в определённых точках жизненного цикла Claude Code. Hooks предоставляют детерминированный контроль над поведением Claude Code, обеспечивая автоматическое выполнение определённых действий.

### Основные возможности Hooks

- **Notifications**: Кастомные уведомления когда Claude ждёт вашего ввода
- **Validation**: Автоматическая проверка кода (linting, formatting)
- **Logging**: Отслеживание всех выполненных команд
- **Feedback**: Автоматическая обратная связь при нарушениях конвенций
- **Custom permissions**: Блокировка изменений production файлов
- **Automation**: Автоматические действия после событий

## Типы Hooks

### 1. SessionStart

Выполняется при старте новой сессии Claude Code.

**Примеры использования:**
- Установка зависимостей
- Запуск dev серверов
- Инициализация окружения
- Проверка версий инструментов

**Конфигурация:**
```json
{
  "hooks": [
    {
      "event": "SessionStart",
      "hooks": [
        {
          "type": "command",
          "command": "npm install",
          "description": "Install dependencies"
        },
        {
          "type": "command",
          "command": "docker-compose up -d",
          "description": "Start dev services"
        }
      ]
    }
  ]
}
```

### 2. SessionEnd

Выполняется при завершении сессии.

**Примеры:**
- Очистка временных файлов
- Остановка dev серверов
- Сохранение логов
- Backup данных

```json
{
  "hooks": [
    {
      "event": "SessionEnd",
      "hooks": [
        {
          "type": "command",
          "command": "docker-compose down",
          "description": "Stop dev services"
        }
      ]
    }
  ]
}
```

### 3. PreToolUse

Выполняется **перед** использованием инструмента.

**Примеры:**
- Валидация команд bash
- Проверка прав доступа
- Логирование действий
- Custom permission logic

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'Executing: $CLAUDE_TOOL_INPUT' >> ~/.claude/bash_log.txt"
        }
      ]
    }
  ]
}
```

**Input переменные:**
- `$CLAUDE_TOOL_NAME`: имя инструмента
- `$CLAUDE_TOOL_INPUT`: JSON с входными данными

**Output:**
Hook может вернуть JSON для контроля выполнения:
```json
{
  "allow": true,      // разрешить выполнение
  "feedback": "..."   // сообщение пользователю
}
```

### 4. PostToolUse

Выполняется **после** использования инструмента.

**Примеры:**
- Автоматическое форматирование после редактирования
- Запуск линтеров
- Коммит изменений
- Уведомления

```json
{
  "hooks": [
    {
      "event": "PostToolUse",
      "matcher": "Edit",
      "hooks": [
        {
          "type": "command",
          "command": "prettier --write \"$CLAUDE_TOOL_INPUT_PATH\"",
          "description": "Auto-format edited file"
        }
      ]
    }
  ]
}
```

**Input переменные:**
- `$CLAUDE_TOOL_NAME`: имя инструмента
- `$CLAUDE_TOOL_INPUT`: входные данные
- `$CLAUDE_TOOL_OUTPUT`: результат выполнения

### 5. Stop

Выполняется когда Claude запрашивает остановку.

**Prompt-based hooks** (используют LLM для принятия решения):

```json
{
  "hooks": [
    {
      "event": "Stop",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Is the current task complete and ready to stop? Consider:\n- Are all files saved?\n- Are tests passing?\n- Is the implementation complete?\n\nRespond with { \"allow\": true/false, \"feedback\": \"reason\" }"
        }
      ]
    }
  ]
}
```

### 6. SubagentStart / SubagentStop

Контроль запуска и остановки субагентов.

## Практические примеры Hooks

### Пример 1: Bash Command Validator

Проверяет bash команды перед выполнением:

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "$HOME/.claude/hooks/validate_bash.sh",
          "description": "Validate bash commands"
        }
      ]
    }
  ]
}
```

**`validate_bash.sh`:**
```bash
#!/bin/bash

# Читаем входные данные
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.command')

# Опасные команды
DANGEROUS=("rm -rf /" "dd if=" ":(){:|:&};:" "mkfs" "chmod -R 777")

for cmd in "${DANGEROUS[@]}"; do
  if [[ "$COMMAND" == *"$cmd"* ]]; then
    echo "{\"allow\": false, \"feedback\": \"Dangerous command blocked: $cmd\"}"
    exit 0
  fi
done

# Разрешить выполнение
echo "{\"allow\": true}"
```

### Пример 2: Auto-format Hook

Автоматическое форматирование после редактирования:

```json
{
  "hooks": [
    {
      "event": "PostToolUse",
      "matcher": "Edit",
      "hooks": [
        {
          "type": "command",
          "command": "$HOME/.claude/hooks/auto_format.sh",
          "description": "Auto-format code"
        }
      ]
    }
  ]
}
```

**`auto_format.sh`:**
```bash
#!/bin/bash

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.filePath')

# Определяем тип файла и применяем нужный formatter
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx)
    prettier --write "$FILE_PATH"
    eslint --fix "$FILE_PATH"
    ;;
  *.py)
    black "$FILE_PATH"
    ;;
  *.go)
    gofmt -w "$FILE_PATH"
    ;;
  *.rs)
    rustfmt "$FILE_PATH"
    ;;
esac
```

### Пример 3: Test Runner Hook

Автоматический запуск тестов после изменений:

```json
{
  "hooks": [
    {
      "event": "PostToolUse",
      "matcher": "Edit",
      "hooks": [
        {
          "type": "command",
          "command": "$HOME/.claude/hooks/run_tests.sh",
          "description": "Run related tests"
        }
      ]
    }
  ]
}
```

**`run_tests.sh`:**
```bash
#!/bin/bash

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.filePath')

# Находим соответствующий тестовый файл
if [[ "$FILE_PATH" == *.test.* ]] || [[ "$FILE_PATH" == *.spec.* ]]; then
  # Это уже тестовый файл, не запускаем
  exit 0
fi

TEST_FILE="${FILE_PATH%.*}.test.${FILE_PATH##*.}"

if [[ -f "$TEST_FILE" ]]; then
  echo "Running tests for $FILE_PATH..."
  npm test -- "$TEST_FILE"
fi
```

### Пример 4: Notification Hook

Уведомление когда Claude ждёт ввода:

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "osascript -e 'display notification \"Claude is waiting for approval\" with title \"Claude Code\"'",
          "description": "Notify on macOS"
        }
      ]
    }
  ]
}
```

### Пример 5: Logging Hook

Детальное логирование всех операций:

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "hooks": [
        {
          "type": "command",
          "command": "$HOME/.claude/hooks/log_action.sh",
          "description": "Log all tool usage"
        }
      ]
    }
  ]
}
```

**`log_action.sh`:**
```bash
#!/bin/bash

LOG_FILE="$HOME/.claude/activity.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.toolName')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.toolInput')

echo "[$TIMESTAMP] Tool: $TOOL_NAME" >> "$LOG_FILE"
echo "Input: $TOOL_INPUT" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"

echo "{\"allow\": true}"
```

## Конфигурация Hooks

### Файлы конфигурации

Hooks конфигурируются в `settings.json`:

**Локации:**
- **User-level:** `~/.claude/settings.json` (применяется ко всем проектам)
- **Project-level:** `.claude/settings.json` (только для текущего проекта)
- **Plugin-level:** Plugins могут предоставлять свои hooks

### Структура конфигурации

```json
{
  "hooks": [
    {
      "event": "SessionStart|SessionEnd|PreToolUse|PostToolUse|Stop|SubagentStart|SubagentStop",
      "matcher": "ToolName",  // только для PreToolUse/PostToolUse
      "hooks": [
        {
          "type": "command|prompt",
          "command": "path/to/script.sh",  // для type: command
          "prompt": "...",                  // для type: prompt
          "description": "What this hook does"
        }
      ]
    }
  ]
}
```

### Matcher patterns

Для `PreToolUse` и `PostToolUse` можно указать matcher:

```json
{
  "matcher": "Bash"        // точное совпадение
}
{
  "matcher": "Edit|Write"  // несколько инструментов (OR)
}
{
  "matcher": ""            // все инструменты (оставьте пустым)
}
```

## Создание Hook через UI

1. Запустите Claude Code: `claude`
2. Выполните: `/config`
3. Перейдите на вкладку **Hooks**
4. Нажмите **Add Hook**
5. Выберите:
   - Event type
   - Hook type (command/prompt)
   - Command/prompt
   - Storage location (User/Project)

## Security Considerations

⚠️ **ВАЖНО:** Hooks выполняются автоматически с вашими credentials!

### Best Practices безопасности

1. **Валидируйте входные данные**
   ```bash
   # НЕ ДЕЛАЙТЕ ТАК:
   eval "$CLAUDE_TOOL_INPUT"
   
   # ДЕЛАЙТЕ ТАК:
   INPUT=$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.command')
   # Валидируйте INPUT перед использованием
   ```

2. **Используйте абсолютные пути**
   ```bash
   # Используйте переменные окружения
   HOOK_DIR="$CLAUDE_PROJECT_DIR/.claude/hooks"
   ```

3. **Ограничивайте выполнение**
   ```bash
   # Разрешайте только конкретные команды
   ALLOWED_COMMANDS=("npm test" "npm run lint")
   ```

4. **Проверяйте источник**
   - Не доверяйте hooks из ненадёжных источников
   - Всегда проверяйте код hooks перед использованием

5. **Используйте sandboxing**
   ```bash
   # Выполняйте в ограниченном окружении
   timeout 30s "$COMMAND"
   ```

## Debugging Hooks

### Basic Troubleshooting

1. **Проверьте syntax JSON**
   ```bash
   cat .claude/settings.json | jq .
   ```

2. **Тестируйте команды отдельно**
   ```bash
   # Запустите hook script вручную
   echo '{"toolName":"Bash","toolInput":"echo test"}' | .claude/hooks/test.sh
   ```

3. **Проверьте permissions**
   ```bash
   chmod +x .claude/hooks/*.sh
   ```

4. **Включите debug mode**
   ```bash
   claude --debug
   ```

### Advanced Debugging

1. **Добавьте логирование в hooks**
   ```bash
   echo "DEBUG: Input=$INPUT" >> /tmp/claude-hook-debug.log
   ```

2. **Валидируйте JSON schemas**
   ```bash
   echo "$OUTPUT" | jq . || echo "Invalid JSON"
   ```

3. **Мониторьте выполнение**
   ```bash
   time "$COMMAND"  # измерить время выполнения
   ```

## Plugin Hooks

Plugins могут предоставлять собственные hooks, которые автоматически интегрируются.

**Пример plugin с hooks:**
```json
{
  "name": "my-plugin",
  "hooks": [
    {
      "event": "PostToolUse",
      "matcher": "Edit",
      "hooks": [
        {
          "type": "command",
          "command": "$PLUGIN_DIR/format.sh"
        }
      ]
    }
  ]
}
```

## Примеры для разных сценариев

### Development Environment Setup

```json
{
  "hooks": [
    {
      "event": "SessionStart",
      "hooks": [
        {"type": "command", "command": "nvm use"},
        {"type": "command", "command": "npm install"},
        {"type": "command", "command": "docker-compose up -d db redis"}
      ]
    }
  ]
}
```

### CI/CD Integration

```json
{
  "hooks": [
    {
      "event": "PostToolUse",
      "matcher": "Edit",
      "hooks": [
        {"type": "command", "command": "npm run lint:fix"},
        {"type": "command", "command": "npm test -- --related"}
      ]
    }
  ]
}
```

### Team Collaboration

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": "Write",
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/check_conventions.sh",
          "description": "Validate team conventions"
        }
      ]
    }
  ]
}
```

## Следующие шаги

- [Субагенты для специализации](./06-subagents.md)
- [Skills для расширения возможностей](./08-skills-and-agents.md)
- [Security best practices](./12-security-and-permissions.md)
