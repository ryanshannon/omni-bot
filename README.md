# OmniAgent

A Dockerized Python 3.11+ multi-agent AI research assistant that aggregates AI research and news, produces daily briefs, and supports configurable LLM routing.

## Current Status: Phase 0 - Hello Brief

The application currently provides:
- Health check endpoint
- Placeholder brief endpoint
- Dockerized environment
- Structured logging

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## Quick Start

1. **Clone and navigate to the repository:**
   ```bash
   cd omni-bot
   ```

2. **Start the application with Docker Compose:**
   ```bash
   docker compose up --build
   ```

3. **Access the application:**
   - Health check: http://localhost:8000/health
   - Latest brief: http://localhost:8000/brief/latest
   - API docs: http://localhost:8000/docs

## Project Structure

```
.
├── Dockerfile              # Container definition
├── docker-compose.yml      # Docker Compose configuration
├── pyproject.toml         # Python dependencies and configuration
├── .env.example           # Environment variables template
├── src/
│   ├── app/              # FastAPI application
│   ├── data/             # Data ingestion and storage (Phase 1+)
│   ├── llm/              # LLM routing and providers (Phase 2+)
│   ├── agents/           # Agent workflow (Phase 4+)
│   └── mcp_clients/      # MCP integrations (Phase 3+)
├── tests/                # Unit and integration tests
├── prompts/              # LLM prompt templates
└── data/                 # Persistent data storage
```

## Development

### Local Setup (without Docker)

1. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

2. **Run the application:**
   ```bash
   uvicorn src.app.main:app --reload
   ```

3. **Run tests:**
   ```bash
   pytest
   ```

### Linting and Formatting

```bash
ruff check .
ruff format .
```

## Roadmap

- **Phase 0** ✅ - Hello Brief: Basic FastAPI app with placeholder endpoints
- **Phase 1** - Arxiv ingestion + SQLite storage
- **Phase 1.5** - Deterministic brief generation (no LLM)
- **Phase 2** - LLM integration with configurable model routing
- **Phase 3** - MCP read-only integrations
- **Phase 4** - Critic and deduplication
- **Phase 5** - Self-improvement loop (Issue → PR workflow)
- **Phase 6** - Auto-restart on merge

## Configuration

Configuration is managed through:
- `.env` file for environment variables
- `sources.yaml` for data sources (Phase 1+)
- `models.yaml` for LLM configuration (Phase 2+)
- Prompt files in `/prompts` (Phase 2+)

## API Endpoints

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### `GET /brief/latest`
Get the latest research brief (currently placeholder).

**Response:**
```json
{
  "content": "...",
  "format": "markdown",
  "generated_at": null
}
```

## License

See LICENSE file for details.

## Contributing

This project follows a phased development approach. See `CLAUDE_CODE_INSTRUCTIONS.md` for implementation guidelines.
