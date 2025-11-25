# Команды и использование Claude Code

## Основные команды CLI

### Запуск Claude Code

```bash
# Интерактивный режим (REPL)
claude

# One-shot команда
claude "your prompt here"

# С конкретным файлом
claude --file path/to/file.ts "Explain this code"

# Verbose mode (подробный вывод)
claude --verbose

# Debug mode
claude --debug
```

### Основные флаги

| Флаг | Описание | Пример |
|------|----------|--------|
| `--version` | Показать версию | `claude --version` |
| `--help` | Показать справку | `claude --help` |
| `--debug` | Режим отладки | `claude --debug` |
| `--verbose` | Подробный вывод | `claude --verbose` |
| `--file <path>` | Указать файл для контекста | `claude --file app.ts` |
| `--no-cache` | Отключить кэширование промптов | `claude --no-cache` |

## Встроенные Slash Commands

Slash commands — это специальные команды, которые начинаются с `/` и предоставляют быстрый доступ к функциям Claude Code.

### Управление сессией

#### `/help`
Показывает список всех доступных команд.
```
/help
```

#### `/resume`
Продолжить предыдущую сессию.
```
/resume
# или с конкретным ID сессии
/resume <session-id>
```

#### `/clear`
Очистить текущий контекст разговора.
```
/clear
```

#### `/exit` или `/quit`
Выйти из интерактивного режима.
```
/exit
```

### Управление контекстом

#### `/context`
Показать текущий контекст (файлы, токены, использование).
```
/context
```

**Вывод:**
```
Current Context:
- Files in context: 5
- Tokens used: 12,450 / 200,000
- Model: claude-3-7-sonnet

Files:
1. src/app.ts (2,340 tokens)
2. src/utils/helper.ts (890 tokens)
...
```

#### `/add <path>`
Добавить файл или директорию в контекст.
```
/add src/components/UserCard.tsx
/add src/utils/
```

#### `/remove <path>`
Удалить файл из контекста.
```
/remove src/components/UserCard.tsx
```

### Конфигурация

#### `/config`
Открыть интерфейс настроек.
```
/config
```

Открывает табовый интерфейс с разделами:
- **Status:** Текущее состояние и статистика
- **Model:** Настройки модели
- **Permissions:** Управление разрешениями
- **Environment:** Переменные окружения
- **Advanced:** Расширенные настройки

#### `/permissions`
Управление разрешениями для инструментов.
```
/permissions
```

Показывает и позволяет изменить:
- Allow rules (автоматическое разрешение)
- Ask rules (запрос подтверждения)
- Deny rules (запрет использования)

#### `/model <model-name>`
Переключить используемую модель.
```
/model claude-3-7-sonnet
/model claude-3-5-sonnet
/model claude-3-opus
```

### Работа с файлами

#### `/read <path>`
Прочитать и показать содержимое файла.
```
/read src/app.ts
```

#### `/write <path>`
Создать или перезаписать файл.
```
/write test.txt
Hello, World!
^D  # Ctrl+D для завершения ввода
```

#### `/search <query>`
Поиск в текущей директории.
```
/search "function processPayment"
/search "TODO"
```

### Git команды

#### `/git status`
Показать статус git репозитория.
```
/git status
```

#### `/git diff`
Показать текущие изменения.
```
/git diff
# или для конкретного файла
/git diff src/app.ts
```

#### `/git log`
Показать историю коммитов.
```
/git log
# последние 10 коммитов
/git log -n 10
```

### Debugging и Troubleshooting

#### `/debug`
Включить/выключить режим отладки.
```
/debug on
/debug off
```

#### `/logs`
Показать логи текущей сессии.
```
/logs
# последние 50 строк
/logs --tail 50
```

#### `/health`
Проверить статус соединения и сервисов.
```
/health
```

## Кастомные Slash Commands

Вы можете создавать собственные slash commands для часто используемых промптов.

### Создание кастомной команды

#### Структура директорий

```
# Проектные команды
.claude/
└── commands/
    ├── review.md
    ├── test.md
    └── frontend/
        └── component.md

# Пользовательские команды (доступны во всех проектах)
~/.claude/
└── commands/
    ├── explain.md
    └── refactor.md
```

#### Формат команды

Файл команды — это Markdown с метаданными YAML:

**`.claude/commands/review.md`:**
```markdown
---
name: review
description: Review code for best practices and potential issues
allowed-tools: Read, Grep, Glob
---

Please review the code in the current context for:

1. Code quality and best practices
2. Potential bugs and edge cases
3. Performance considerations
4. Security vulnerabilities
5. Documentation completeness

Provide specific feedback with:
- Line numbers for issues
- Explanation of problems
- Suggested fixes
- Priority level (critical/important/minor)

Format findings as a checklist.
```

### Использование кастомных команд

```bash
# Просто вызовите по имени
/review

# С аргументами
/test --coverage

# Список всех кастомных команд
/commands
```

### Параметры команды

#### Основные поля YAML

```yaml
---
name: command-name              # Имя команды (обязательно)
description: Short description  # Описание для /help
allowed-tools: Read, Write     # Разрешенные инструменты
denied-tools: Bash             # Запрещенные инструменты
---
```

#### Параметры в командах

Используйте `$1`, `$2`, и т.д. для аргументов:

**`.claude/commands/generate-test.md`:**
```markdown
---
name: gen-test
description: Generate tests for a file
---

Generate comprehensive unit tests for the file: $1

Include:
- Happy path tests
- Edge cases
- Error scenarios
- Mock external dependencies
```

**Использование:**
```bash
/gen-test src/utils/payment.ts
# $1 будет заменено на "src/utils/payment.ts"
```

#### Bash команды в промпте

Можно выполнять bash команды и включать их вывод:

```markdown
---
name: recent-changes
description: Analyze recent changes
allowed-tools: Bash
---

Analyze the following recent changes:

!git log --oneline -10
!git diff HEAD~5..HEAD --stat

What are the main themes of these changes?
```

Команды с префиксом `!` выполняются, и их вывод включается в промпт.

### Namespacing команд

Организуйте команды в поддиректории:

```
.claude/commands/
├── frontend/
│   ├── component.md     # /component (project:frontend)
│   └── page.md          # /page (project:frontend)
├── backend/
│   ├── api.md           # /api (project:backend)
│   └── service.md       # /service (project:backend)
└── review.md            # /review (project)

~/.claude/commands/
└── explain.md           # /explain (user)
```

При конфликте имен, описание показывает источник:
- `(user)` — пользовательская команда
- `(project)` — проектная команда
- `(project:subdirectory)` — из поддиректории

### SlashCommand Tool

Claude может автоматически вызывать ваши кастомные команды:

```
"Can you review this code using our review command?"
# Claude автоматически вызовет /review если подходит
```

Чтобы увидеть какие команды доступны для `SlashCommand` tool:
```bash
claude --debug
# Затем выполните запрос
# В debug output будет список доступных команд
```

### Примеры полезных команд

#### Code Review команда

**`.claude/commands/review.md`:**
```markdown
---
name: review
description: Comprehensive code review
allowed-tools: Read, Grep, Glob
---

Perform a thorough code review:

## Code Quality
- [ ] Follows project conventions
- [ ] Proper error handling
- [ ] No code smells

## Testing
- [ ] Has appropriate test coverage
- [ ] Tests cover edge cases

## Documentation
- [ ] Functions have JSDoc
- [ ] Complex logic is explained

## Security
- [ ] No hardcoded secrets
- [ ] Proper input validation
- [ ] No SQL injection risks

## Performance
- [ ] No obvious bottlenecks
- [ ] Efficient algorithms used

Provide specific line numbers and suggestions.
```

#### Generate Component команда

**`.claude/commands/frontend/component.md`:**
```markdown
---
name: component
description: Generate React component with TypeScript
---

Create a React TypeScript component: $1

Requirements:
- Use functional component with hooks
- Include TypeScript interfaces for props
- Add JSDoc documentation
- Include basic styling setup
- Export component as default
- Add prop-types for runtime validation

File location: src/components/$1.tsx
```

**Использование:**
```bash
/component UserProfile
# Создаст компонент UserProfile
```

#### Generate Tests команда

**`.claude/commands/test.md`:**
```markdown
---
name: test
description: Generate tests for file
allowed-tools: Read, Write
---

!cat $1

Generate comprehensive tests for the above code:

1. **Unit tests** for all exported functions
2. **Edge cases** testing
3. **Error scenarios** testing
4. **Integration tests** if applicable

Use the project's test framework (check package.json).
Create test file: $1.test.ts
```

## Работа с разрешениями через команды

### Просмотр текущих разрешений

```bash
/permissions
```

### Разрешить инструмент

```bash
# Разрешить Bash команды без подтверждения
/allow Bash

# Разрешить конкретную команду
/allow Bash "npm test"
/allow Bash "git status"
```

### Запретить инструмент

```bash
# Запретить выполнение bash команд
/deny Bash

# Запретить редактирование конкретных файлов
/deny Write "*.env"
/deny Write "package-lock.json"
```

### Сбросить разрешения

```bash
# Сбросить все к дефолтным
/permissions reset
```

## Advanced Usage

### Работа с multiple сессиями

```bash
# Список активных сессий
/sessions

# Переключиться на сессию
/session <id>

# Создать новую сессию
/new-session
```

### Экспорт и импорт настроек

```bash
# Экспорт настроек
claude config export > my-config.json

# Импорт настроек
claude config import my-config.json
```

### Работа с окружениями

```bash
# Установить переменную окружения для сессии
/env set API_URL=http://localhost:3000

# Показать все переменные
/env list

# Удалить переменную
/env unset API_URL
```

## Workflow Examples

### Полный цикл разработки функции

```bash
# 1. Создать ветку
claude "Create a new branch: feature/user-notifications"

# 2. Реализовать функцию
claude "Implement real-time notifications using WebSockets"

# 3. Добавить тесты
/test src/notifications/NotificationService.ts

# 4. Code review
/review

# 5. Запустить тесты
claude "Run all tests"

# 6. Commit и push
claude "Commit changes and push to remote"

# 7. Создать PR
claude "Create PR with description of changes"
```

### Debug workflow

```bash
# 1. Проанализировать ошибку
claude "TypeError: Cannot read property 'map' of undefined in UserList.tsx:45"

# 2. Показать контекст
/read src/components/UserList.tsx

# 3. Исправить
claude "Fix this issue"

# 4. Тестировать
claude "Run relevant tests"

# 5. Commit
claude "Commit the fix"
```

## Best Practices

### 1. Используйте алиасы

Создайте алиасы для часто используемых команд:

```bash
# В ~/.bashrc или ~/.zshrc
alias cr="claude 'Code review current changes'"
alias ct="claude 'Run tests'"
alias cf="claude 'Fix linting issues'"
```

### 2. Создавайте команды для рутинных задач

Вместо повторения одних и тех же промптов, создайте slash команды.

### 3. Документируйте команды

Добавьте хорошее описание в YAML frontmatter для каждой команды.

### 4. Используйте namespacing

Организуйте команды по категориям (frontend/, backend/, testing/, и т.д.)

### 5. Управляйте разрешениями

Настройте allow/deny правила для безопасности.

## Следующие шаги

- [Hooks для расширенной кастомизации](./05-hooks-and-customization.md)
- [Skills для специализированных возможностей](./08-skills-and-agents.md)
- [Plugins для расширения функционала](./09-plugins-and-marketplaces.md)
