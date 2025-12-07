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
- Commit working code after completing each phase or major milestone.

## Git Workflow
Follow these git practices throughout development:

### Branching Strategy
- **main**: Production-ready code. Each phase completion merges here.
- **phase-N**: Feature branch for each major phase (e.g., `phase-1-arxiv`, `phase-2-llm`)
- **fix/**: Hotfix branches for urgent bug fixes
- Create feature branches from main, merge back via PR when phase is complete

### Commit Conventions
Use clear, descriptive commit messages following this format:
```
<type>(<scope>): <subject>

<optional body>
```

Types:
- `feat`: New feature (e.g., "feat(api): add brief endpoint")
- `fix`: Bug fix
- `refactor`: Code restructuring without functionality change
- `test`: Adding or updating tests
- `docs`: Documentation changes
- `chore`: Maintenance tasks (dependencies, config)
- `build`: Build system changes (Docker, dependencies)

Examples:
- `feat(phase-0): implement FastAPI health and brief endpoints`
- `build(docker): add Dockerfile and compose configuration`
- `test(api): add tests for health and brief endpoints`
- `docs(readme): add setup and run instructions`

### When to Commit
- **After each phase completion**: Commit when all acceptance criteria pass
- **After significant sub-tasks**: Don't wait for the entire phase if you've completed a logical chunk
- **Before switching contexts**: Commit working state before starting a different task
- **When tests pass**: Never commit broken code or failing tests

### Phase Completion Checklist
When completing each phase:
1. Ensure all acceptance criteria are met
2. Run all tests and verify they pass
3. Update README if user-facing changes exist
4. Commit changes with descriptive message
5. Create PR from phase branch to main (if using branches)
6. Manual review and testing
7. Merge to main
8. Tag release with phase number (e.g., `v0.1-phase-0`)

### Before Phase 5
- Git commits are manual and deliberate
- No automated git operations
- All commits reviewed by human before pushing

### Phase 5 and Beyond
- The self-improvement loop will automate: Issue → Branch → Code → Test → PR
- Human review required before merge
- Never auto-merge to main without approval

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
- Tests included and passing
- README updated if usage changes
- Code committed to git with descriptive message
- If phase complete: branch ready for PR/merge to main
