# OmniAgent Development TODO

This document tracks the progress of all development phases for OmniAgent.

## Legend
- ✅ Complete
- 🔄 In Progress
- ⏳ Pending
- ⏸️ Blocked

---

## Phase 0 — Hello Brief ✅

**Status:** Complete
**Branch:** main
**Commit:** `5db13c3`

### Tasks
- ✅ Create FastAPI app with `/health` endpoint
- ✅ Create FastAPI app with `/brief/latest` endpoint (placeholder)
- ✅ Implement Dockerfile
- ✅ Implement docker-compose.yml
- ✅ Add structured logging (structlog)
- ✅ Create README with run steps
- ✅ Add basic tests for endpoints
- ✅ Verify `docker compose up` works
- ✅ Verify /brief/latest accessible in browser

### Acceptance Criteria
- ✅ `docker compose up` works
- ✅ /brief/latest is visible in browser/phone
- ✅ Tests pass
- ✅ Code committed to git

---

## Phase 1 — Arxiv Ingestion + SQLite ⏳

**Status:** Pending
**Branch:** TBD
**Target:** Fetch and persist Arxiv papers

### Tasks
- ⏳ Create `sources.yaml` with Arxiv configuration
- ⏳ Implement Arxiv HTTP client (or use lightweight library)
- ⏳ Define minimal schema for papers:
  - id, title, authors, published_at, summary, url, source
- ⏳ Implement SQLite repository
  - Create schema/migrations
  - CRUD operations for papers
- ⏳ Configure SQLite storage in volume path (`./data` or `/app/data`)
- ⏳ Create ingestion service/command to fetch papers
- ⏳ Add unit tests (mock network calls)
- ⏳ Verify persistence across container restart
- ⏳ Update README if needed
- ⏳ Commit changes when tests pass

### Acceptance Criteria
- ⏳ Command/function can fetch and store newest N papers
- ⏳ Data persists across container restart
- ⏳ Unit tests mock network calls
- ⏳ All tests pass

---

## Phase 1.5 — Brief Generation (No LLM) ⏳

**Status:** Pending
**Branch:** TBD
**Target:** Generate deterministic briefs from stored papers

### Tasks
- ⏳ Implement deterministic summarizer service
  - Select top N newest papers from DB
  - Format as Markdown brief
- ⏳ Save brief to `data/latest_brief.md`
- ⏳ Update `/brief/latest` endpoint to read from file
- ⏳ Add route to render markdown properly
- ⏳ Add tests for brief generation logic
- ⏳ Test end-to-end: ingest → generate → view
- ⏳ Update README if needed
- ⏳ Commit changes when tests pass

### Acceptance Criteria
- ⏳ UI shows a generated brief from real data
- ⏳ Brief updates when new papers are ingested
- ⏳ All tests pass

---

## Phase 2 — LLM Integration + ModelRouter ⏳

**Status:** Pending
**Branch:** TBD
**Target:** Add configurable LLM for better summaries

### Tasks
- ⏳ Create `models.yaml` configuration file
- ⏳ Design `ModelRouter` interface/abstract class
- ⏳ Implement Google GenAI provider adapter
- ⏳ (Optional) Implement local HTTP endpoint adapter
- ⏳ Create prompt templates in `/prompts` directory
- ⏳ Integrate LLM into brief generation
- ⏳ Add environment variables for API keys
- ⏳ Update `.env.example` with new variables
- ⏳ Mock LLM calls in tests
- ⏳ Verify model switching via config only
- ⏳ Update README with LLM setup instructions
- ⏳ Commit changes when tests pass

### Acceptance Criteria
- ⏳ Switching model/provider requires config change only
- ⏳ Tests mock router calls
- ⏳ LLM-generated briefs are more coherent
- ⏳ All tests pass

---

## Phase 3 — MCP (Read-only) ⏳

**Status:** Pending
**Branch:** TBD
**Target:** Add MCP integrations for reading external data

### Tasks
- ⏳ Research/select MCP client library
- ⏳ Implement GitHub MCP wrapper (read issues)
- ⏳ (Optional) Implement Fetch MCP wrapper
- ⏳ Integrate MCP clients into workflow orchestration
- ⏳ Add configuration for MCP servers
- ⏳ Create dev/testing mode to list GitHub issues
- ⏳ Add tests with mocked MCP responses
- ⏳ Update README with MCP setup
- ⏳ Commit changes when tests pass

### Acceptance Criteria
- ⏳ Agent can list open GitHub issues via MCP in dev mode
- ⏳ MCP integrations are read-only
- ⏳ All tests pass

---

## Phase 4 — Critic + Dedupe ⏳

**Status:** Pending
**Branch:** TBD
**Target:** Add quality control and deduplication

### Tasks
- ⏳ Create critic prompt with quality rubric
- ⏳ Implement critic service/agent
- ⏳ Add rewrite workflow when critic rejects
- ⏳ Implement deduplication service
  - Paper title/content similarity
  - Remove duplicate entries
- ⏳ Integrate critic into brief generation pipeline
- ⏳ Add tests for critic logic
- ⏳ Add tests for deduplication
- ⏳ Update README if needed
- ⏳ Commit changes when tests pass

### Acceptance Criteria
- ⏳ Critic can force rewrite path
- ⏳ Duplicate papers are filtered out
- ⏳ All tests pass

---

## Phase 5 — Self-Improvement Loop ⏳

**Status:** Pending
**Branch:** TBD
**Target:** Automated Issue → PR workflow with human approval

### Tasks
- ⏳ Design agent architecture:
  - TriageAgent (analyze issues)
  - ArchitectAgent (design solution)
  - EngineerAgent (write code)
  - QAAgent (run tests in sandbox)
- ⏳ Implement TriageAgent
- ⏳ Implement ArchitectAgent
- ⏳ Implement EngineerAgent
- ⏳ Implement QAAgent with sandbox runner
- ⏳ Create workflow orchestration
- ⏳ Implement PR creation (only when tests pass)
- ⏳ Add safeguards (no auto-merge)
- ⏳ Extensive testing of workflow
- ⏳ Update README with workflow documentation
- ⏳ Commit changes when tests pass

### Acceptance Criteria
- ⏳ Basic Issue → PR flow works end-to-end
- ⏳ Tests must pass before PR creation
- ⏳ Human review required before merge
- ⏳ No auto-merge to main
- ⏳ All tests pass

---

## Phase 6 — Auto-Restart ⏳

**Status:** Pending
**Branch:** TBD
**Target:** Container updates automatically on merge

### Tasks
- ⏳ Add Watchtower service to docker-compose.yml
- ⏳ Configure Watchtower for local development
- ⏳ Document GitHub Actions expectations
- ⏳ Create GitHub Actions workflow (if needed)
- ⏳ Test merge → rebuild → restart flow
- ⏳ Update README with auto-restart docs
- ⏳ Commit changes when tests pass

### Acceptance Criteria
- ⏳ Merge to main causes container update locally
- ⏳ Application restarts automatically
- ⏳ All tests pass

---

## Current Blockers

*None currently*

---

## Notes & Decisions

### Phase 0 (Completed)
- Used FastAPI for web framework
- Used structlog for structured logging
- Docker Compose for local development
- Pytest for testing

### Upcoming Decisions
- **Phase 1**: Choose Arxiv library (feedparser vs custom HTTP)
- **Phase 2**: Confirm Google GenAI as first LLM provider
- **Phase 4**: Define similarity threshold for deduplication
- **Phase 5**: Select sandbox technology (Docker-in-Docker, separate container, etc.)

---

## Quick Reference

**Current Phase:** Phase 0 ✅ Complete
**Next Phase:** Phase 1 - Arxiv Ingestion
**Last Updated:** 2025-12-07
