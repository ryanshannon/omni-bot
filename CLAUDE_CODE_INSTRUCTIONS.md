# Claude Code Instructions — OmniAgent

You are Claude Code working on "OmniAgent", a Python 3.11+ multi-agent AI research assistant.
This repo is built with a phased, vertical-slice approach optimized for fast validation.
Your job is to implement the next smallest slice that produces a working, testable increment.

## High-Level Goal
Create a Dockerized application that:
1) Aggregates AI research/news (start with Arxiv),
2) Produces a daily brief in a mobile-friendly web UI,
3) Supports configurable LLM routing,
4) Later adds MCP tool integrations,
5) Eventually supports safe self-improvement via:
   GitHub Issue → Spec → Code → Tests in sandbox → PR → Human review → Merge → Auto-restart.

## Non-Negotiables
- No self-modifying or GitHub write automation until Phase 5 tasks explicitly say so.
- Deterministic tasks must be implemented as plain Python services/functions first.
- LLM calls must be abstracted behind interfaces and mockable.
- Config (sources, models, prompts) must be data-driven files, not code constants.
- Keep dependencies minimal.
- Always add tests for new modules.

## What to Build First
Follow this exact phase order. If anything is missing, create the smallest scaffolding needed.

### Phase 0 — Hello Brief
Implement:
- FastAPI app:
  - GET /health -> {"status":"ok"}
  - GET /brief/latest -> placeholder text
- Dockerfile
- docker-compose.yml
- README run steps
- Basic structured logging

Acceptance:
- `docker compose up` works
- /brief/latest is visible in browser/phone

### Phase 1 — Arxiv ingestion + SQLite
Implement:
- `sources.yaml` with Arxiv config
- Arxiv client (use an HTTP approach or a small library)
- Normalize output into a minimal schema:
  - id, title, authors, published_at, summary, url, source
- SQLite repository stored in a volume path:
  - ./data or /app/data

Acceptance:
- Command/function can fetch and store newest N papers
- Persist across container restart
- Unit tests mock network

### Phase 1.5 — Brief generation without LLM
Implement:
- A deterministic summarizer that:
  - selects top N newest items
  - formats a Markdown brief
- Save to `data/latest_brief.md`
- Web route to render markdown

Acceptance:
- UI shows a generated brief

### Phase 2 — LLM integration + ModelRouter
Implement:
- `models.yaml`
- `ModelRouter` with provider adapters:
  - Google GenAI first
  - Optional local HTTP endpoint
- Prompt files in /prompts

Acceptance:
- Switching model/provider requires config change only
- Tests mock router calls

### Phase 3 — MCP (Read-only)
Implement:
- Add MCP client wrappers for:
  - GitHub (read issues)
  - Fetch (optional)
- Integrate only into workflow orchestration

Acceptance:
- Agent can list open issues via MCP in dev mode

### Phase 4 — Critic + Dedupe
Implement:
- Critic step with rubric prompt
- Dedupe service

Acceptance:
- Critic can force rewrite path

### Phase 5 — Self-Improvement Loop
Implement:
- TriageAgent
- ArchitectAgent
- EngineerAgent
- QAAgent sandbox runner
- PR creation only when tests pass

Acceptance:
- Basic Issue → PR flow works

### Phase 6 — Auto-Restart
Implement:
- Watchtower in compose
- Document GitHub Actions expectations

Acceptance:
- Merge causes container update locally

## Implementation Guardrails
- Prefer simple, explicit code over clever patterns.
- Use clear module boundaries:
  - app/web/config/logging
  - data/ingestion/repository/dedupe
  - llm/router/providers
  - agents/workflow
  - mcp_clients

## Suggested Target Structure
(If missing, create it gradually.)
.
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
├── .env.example
├── sources.yaml
├── models.yaml
├── prompts/
├── src/
│   ├── app/
│   ├── data/
│   ├── llm/
│   ├── agents/
│   └── mcp_clients/
└── tests/

## Testing Expectations
- All new ingestion and repository logic must have unit tests.
- LLM calls must be behind interfaces and fully mockable.
- Add smoke tests for FastAPI routes.

## How to Respond to Ambiguity
If ambiguous:
- Choose the simplest implementation consistent with Phase 0–2.
- Avoid introducing Postgres/pgvector before Phase 4.
- Avoid adding MCP dependencies before Phase 3.

## Definition of Done for Each Slice
- One new working capability visible in:
  - CLI output OR
  - Web UI
- Docker build still works
- Tests included
- README updated if usage changes
