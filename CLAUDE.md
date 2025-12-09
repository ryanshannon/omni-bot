# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OmniAgent is a Dockerized Python 3.11+ multi-agent AI research assistant that aggregates AI research from sources like Arxiv, produces daily briefs, and will eventually support safe self-improvement via GitHub Issues → PR workflow with human approval.


## Essential Commands

> Shell note: Default dev shell is Windows PowerShell (v5.1). Use `;` to chain commands. For POSIX-style `&&/||`, use PowerShell 7+ or WSL.

### Running the Application
```bash
# Start with Docker (recommended)
docker compose up --build

# Local development (without Docker)
pip install -e ".[dev]"
uvicorn src.app.main:app --reload
```

PowerShell variant (explicit shell tag):
```powershell
# Start with Docker (recommended)
docker compose up --build;

# Local development (without Docker)
pip install -e ".[dev]";
uvicorn src.app.main:app --reload;
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

PowerShell chaining example:
```powershell
pytest;
pytest -v;
```

### Code Quality
```bash
# Check linting
ruff check .

# Format code
ruff format .
```

PowerShell chaining example:
```powershell
ruff check .;
ruff format .;
```

## Developer Environment (Windows / PowerShell)

- Host OS & shell: Windows (default shell: PowerShell 5.1). Prefer PowerShell 7+ or WSL for POSIX-friendly behavior.
- Command chaining: Use `;` in PowerShell 5.1. `&&/||` work in PowerShell 7+ and POSIX shells but not 5.1.
- Paths: Prefer repo-relative paths. If absolute paths are needed, provide both `C:\path\to\repo` and `/path/to/repo` variants.
- Quoting: PowerShell single quotes are literal; double quotes interpolate. Label code blocks with `powershell` vs `bash` when examples differ.

Example (PowerShell 5.1):
```powershell
docker compose down; docker compose up --build;
```

Example (bash/WSL):
```bash
docker compose down && docker compose up --build
```

## Architecture & Structure

### Module Organization
The codebase follows a phased vertical-slice architecture with clear separation:

- **`src/app/`** - FastAPI application layer
  - `main.py`: FastAPI app, routes, and exception handlers
  - `config.py`: Pydantic settings (reads from environment)
  - `logging_config.py`: Structlog configuration
  - `models.py`: Pydantic response models
  - `exceptions.py`: Custom exception classes

- **`src/data/`** - Data ingestion and storage (Phase 1+)
- **`src/llm/`** - LLM routing and providers (Phase 2+)
- **`src/agents/`** - Agent workflow orchestration (Phase 4+)
- **`src/mcp_clients/`** - MCP tool integrations (Phase 3+)

### Configuration Management
- Environment variables loaded via Pydantic Settings (`src/app/config.py`)
- Future config files: `sources.yaml`, `models.yaml` (Phase 1-2)
- Prompt templates will live in `/prompts` directory (Phase 2+)
- Docker volumes mount `./data`, `./src`, `./prompts`, `./tests`
- Secrets: Never hardcode keys. `.env` is untracked; `.env.example` is the template. Add new env vars to `.env.example` and document defaults.

### Logging
Uses `structlog` for structured logging throughout. Call `structlog.get_logger()` and use key-value pairs:
```python
logger.info("event_name", key1=value1, key2=value2)
```

## Phased Development Approach

The project follows a strict phased delivery model. **Always consult `docs/TODO.md`** for current phase status and next tasks. Key principles:

1. **No self-modifying code until Phase 5** - GitHub write operations (PR creation) are explicitly forbidden until Phase 5
2. **Deterministic first** - Implement plain Python services before adding LLM calls
3. **LLM calls must be mockable** - Abstract behind interfaces for testing
4. **Data-driven config** - Never hardcode sources, models, or prompts in code
5. **Minimal dependencies** - Only add what's necessary for current phase

### Phase Sequence
0. Hello Brief (✅ Complete)
1. Arxiv ingestion + SQLite
2. LLM integration + ModelRouter
3. MCP read-only integrations
4. Critic + deduplication
5. Self-improvement loop (Issue → PR with human approval)
6. Auto-restart on merge

## Git Workflow

### Commit Message Format
```
<type>(<scope>): <subject>

<optional body>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `build`

Examples:
- `feat(arxiv): add paper ingestion service`
- `test(api): add tests for brief endpoint`

### When to Commit
- After each phase completion (all acceptance criteria met)
- After significant sub-tasks (don't wait for entire phase)
- When all tests pass
- Before context switching

### Important Git Constraints
- **Before Phase 5:** All git operations are manual and require human approval
- **No automated PRs or merges** until Phase 5 explicitly enables it
- Never skip hooks (`--no-verify`) unless explicitly requested
- Never force push to main/master

## Testing Requirements

- **Unit tests required** for all new data ingestion, repository, and business logic
- **Mock external APIs and LLM calls** - use pytest fixtures and mocks
- **Smoke tests for FastAPI routes** - use `httpx` test client
- Tests use async pytest (`asyncio_mode = "auto"` in pyproject.toml)

Example test pattern:
```python
from httpx import AsyncClient
from src.app.main import app

async def test_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
```

## Critical Constraints

1. **No secrets in code** - Use `.env` files (`.env.example` for templates)
2. **No over-engineering** - Implement only what the current phase requires
3. **Prefer simple, explicit code** over clever abstractions
4. **SQLite for persistence** (Phase 1-3) - Don't introduce Postgres/pgvector early
5. **Volume-mounted data** at `./data` or `/app/data` for persistence

## Definition of Done

Quick checklist (run before committing):
- Tests pass: `pytest`
- Docker build/run checked: `docker compose up --build`
- `docs/TODO.md` updated (progress, blockers)
- README updated if user-facing change
- No secrets committed; `.env.example` updated when env vars change

Each task/phase is complete when:
- All acceptance criteria met
- Tests pass (`pytest`)
- Docker build works (`docker compose up`)
- README updated (if user-facing changes)
- `docs/TODO.md` updated with progress
- Code committed with descriptive message
- If phase complete: ready for PR/merge to main

## Key Files to Reference

- **`CLAUDE_CODE_INSTRUCTIONS.md`** - Detailed implementation guidelines and phase specifications
- **`docs/TODO.md`** - Current progress tracking and next tasks
- **`.github/copilot-instructions.md`** - Additional architectural guidance
- **`README.md`** - User-facing documentation and quick start

## Common Patterns

### Adding a New API Endpoint
1. Define Pydantic response model in `src/app/models.py`
2. Add route in `src/app/main.py` with type hints
3. Use structlog for logging events
4. Add test in `tests/test_api.py`

### Adding New Business Logic (Phase 1+)
1. Create module in appropriate subdirectory (`data/`, `llm/`, etc.)
2. Keep interfaces testable (dependency injection)
3. Mock external dependencies
4. Add unit tests in `tests/`

### Environment Variables
1. Add to `src/app/config.py` as Pydantic field
2. Document in `.env.example`
3. Load via `settings` instance (imported from config)
