# GitHub Copilot Agent Instructions — OmniAgent

You are GitHub Copilot Agent working on "OmniAgent", a Dockerized, Python-based AI research/news assistant.
The app uses the Microsoft Agent Framework and will later integrate MCP servers.
The project is built in small vertical slices with strict safety constraints.

## North Star
Build a self-evolving AI research agent that:
1) Aggregates AI papers/news (starting with Arxiv),
2) Produces a daily brief in a mobile-friendly web UI,
3) Supports configurable model routing,
4) Later uses GitHub Issues as the backlog for safe self-improvement:
   Issue → Spec → Code → Tests in sandbox → PR (human review) → Merge → Auto-restart.

## Key Constraints
- Do NOT introduce self-modifying code until Phase 5 tasks explicitly say so.
- Default behaviors must be deterministic where possible.
- Any live GitHub write operations (PR creation) should be stubbed/mocked until Phase 3+.
- Secrets must never be hardcoded. Use env vars and `.env.example`.
- Prefer minimal dependencies.
- Keep code testable without an LLM present (mock model calls).
- `.env` is untracked; `.env.example` is the template. Add new env vars there and keep secrets out of code and YAML.

## Developer Environment (Windows / PowerShell)

- Host OS & shell: Windows (default shell: PowerShell 5.1). Prefer PowerShell 7+ or WSL for POSIX-friendly behavior.
- Command chaining: Use `;` in PowerShell 5.1. `&&/||` work in PowerShell 7+ and POSIX shells but not 5.1.
- Paths: Prefer repo-relative paths. If absolute paths are needed, provide both `C:\path\to\repo` and `/path/to/repo` variants.
- Quoting: PowerShell single quotes are literal; double quotes interpolate. Label code blocks with `powershell` vs `bash` when examples differ.
- Provide both PowerShell and POSIX examples when commands differ; default to shell-agnostic commands when possible.

## Recommended Stack
- Python 3.11+
- FastAPI (preferred) or aiohttp
- pytest
- SQLite for Phase 1–2 persistence
- Docker + docker-compose
- Microsoft Agent Framework (`agent-framework`)
- Google GenAI SDK integration added in Phase 2
- MCP integration added in Phase 3

## Testing & Logging Quickstart
- Async FastAPI tests: use `httpx.AsyncClient(app=app, base_url="http://test")` and `asyncio_mode = "auto"` (already in pyproject).
- Run tests: `pytest` (PowerShell chain with `;` if combining commands).
- Logging: use `structlog.get_logger()` and emit key-value pairs, e.g., `logger.info("event", key=value)`.
- Mock external calls (Arxiv, LLMs) in tests; keep model/router behind interfaces for easy mocking.

## Repository Structure (Target)
.
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
├── .env.example
├── sources.yaml
├── models.yaml
├── prompts/
│   ├── editor.md
│   ├── critic.md
│   └── triage.md
├── src/
│   ├── app/
│   │   ├── main.py
│   │   ├── web.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── data/
│   │   ├── schema.py
│   │   ├── arxiv_client.py
│   │   ├── repository.py
│   │   └── dedupe.py
│   ├── llm/
│   │   ├── router.py
│   │   └── google_client.py
│   ├── agents/
│   │   ├── workflow.py
│   │   ├── topic_selector.py
│   │   ├── researcher.py
│   │   ├── editor.py
│   │   ├── critic.py
│   │   ├── triage.py
│   │   ├── architect.py
│   │   ├── engineer.py
│   │   └── qa.py
│   └── mcp_clients/
│       ├── github_client.py
│       └── fetch_client.py
└── tests/

## Phased Delivery Rules
Each phase must be a working product with tests and README updates.

### Phase 0 — Hello Brief
Implement:
- FastAPI app with routes:
  - GET /health
  - GET /brief/latest (returns placeholder)
- Dockerfile + compose

Acceptance:
- `docker compose up` exposes port 8080
- /brief/latest returns placeholder text

### Phase 1 — Arxiv ingestion + SQLite
Implement:
- sources.yaml
- Arxiv fetcher
- Normalize to PaperItem schema
- Store in SQLite in a volume-mounted path

Acceptance:
- Fetch N newest papers for a query
- Persist across restart

### Phase 1.5 — Brief generation without LLM
Implement:
- Template-based summarizer to produce data/latest_brief.md

Acceptance:
- UI displays generated markdown

### Phase 2 — LLM + ModelRouter
Implement:
- ModelRouter class
- Google GenAI client wrapper
- Optional local endpoint support
- prompts as files

Acceptance:
- Change model via config without code edits
- Model calls are mockable in tests

### Phase 3 — MCP Integration
Implement:
- Read GitHub Issues via MCP client
- Optional fetch MCP client

Acceptance:
- List open issues through MCP in an integration test (can be skipped in CI)

### Phase 4 — Critic + Dedupe
Implement:
- CriticAgent rubric-based review
- URL/title dedupe

Acceptance:
- Critic can trigger rewrite
- Dedupe prevents same item in consecutive runs

### Phase 5 — Self-Improvement Loop (Safe)
Implement:
- TriageAgent: Research vs Code
- ArchitectAgent: generates a mini-spec
- EngineerAgent: writes code changes
- QAAgent: runs pytest in sandbox container
- Open PR only if tests pass

Acceptance:
- Issue "Add X source" → PR opened after green tests

### Phase 6 — Auto-Restart
Implement:
- GitHub Actions build/push
- Watchtower in compose

Acceptance:
- Merge PR triggers container update locally

## Coding Style
- Type hints encouraged
- Dataclasses for schemas
- Clear separation of concerns
- Prefer small functions and explicit interfaces

## Testing Rules
- Unit tests required for core logic
- Mock external APIs and LLMs
- Add at least one happy-path integration test per phase

## Definition of Done
- Quick checklist before commit/PR:
  - Tests pass: `pytest`
  - Docker build/run: `docker compose up --build`
  - `docs/TODO.md` updated (progress, blockers)
  - README updated if user-facing change
  - No secrets committed; `.env.example` updated when env vars change

- Tests pass
- Docker build works
- README updated
- No secrets in code
